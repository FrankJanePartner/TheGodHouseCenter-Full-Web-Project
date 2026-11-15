import logging
from datetime import timedelta
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.middleware.csrf import rotate_token
from django.shortcuts import get_object_or_404
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.cache import never_cache
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .chat_auth import CHAT_SESSION_KEY, attach_chat_session, chat_user, require_chat_user, session_payload
from .models import ChatRoom, ChatUsers, CurrentSeries, Message, NextLive, UserPresence
from .serializers import (
    ChatRoomSerializer,
    ChatUserSerializer,
    CurrentSeriesSerializer,
    GuestLoginSerializer,
    MessageContentSerializer,
    MessageSerializer,
    MessageUpdateSerializer,
    NextLiveSerializer,
    PresenceSerializer,
    WholeWordPartnersSerializer,
)


logger = logging.getLogger(__name__)
RECENT_MESSAGE_LIMIT = 100
PRESENCE_LIFETIME = timedelta(seconds=60)
TYPING_LIFETIME = timedelta(seconds=12)


class GuestThrottle(AnonRateThrottle):
    rate = "20/hour"
    scope = "wwtv-guest"


class PartnershipThrottle(AnonRateThrottle):
    rate = "10/hour"
    scope = "wwtv-partnership"


@never_cache
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def current_user(request):
    return Response(session_payload(request, chat_user(request)))


@never_cache
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([GuestThrottle])
def guest_login(request):
    SessionAuthentication().enforce_csrf(request)
    serializer = GuestLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    values = serializer.validated_data

    # An unverified address is contact information only and cannot identify an existing account.
    user = ChatUsers.objects.create(fullname=values["fullname"], contact_email=values["email"])
    attach_chat_session(request, user)
    return Response(session_payload(request, user), status=status.HTTP_201_CREATED)


@never_cache
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def logout(request):
    SessionAuthentication().enforce_csrf(request)
    user_id = request.session.pop(CHAT_SESSION_KEY, None)
    if user_id is not None:
        UserPresence.objects.filter(chat_user_id=user_id).update(is_online=False, is_typing=False)
        request.session.cycle_key()
        rotate_token(request)
    return Response(session_payload(request, None))


@never_cache
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def chat_status(request):
    room_id = (
        ChatRoom.objects.filter(is_active=True).order_by("pk").values_list("pk", flat=True).first()
    )
    return Response({"is_on": room_id is not None, "room_id": room_id})


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def chat_room_list(request):
    return Response(ChatRoomSerializer(ChatRoom.objects.order_by("pk"), many=True).data)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def chat_room_detail(request, pk):
    return Response(ChatRoomSerializer(get_object_or_404(ChatRoom, pk=pk)).data)


@never_cache
@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def room_messages(request, room_id):
    room = get_object_or_404(ChatRoom, pk=room_id, is_active=True)
    if request.method == "GET":
        recent = Message.objects.filter(room=room, hidden_at__isnull=True).order_by("-created_at", "-pk")
        messages = list(recent[:RECENT_MESSAGE_LIMIT])
        return Response(MessageSerializer(messages[::-1], many=True).data)

    user = require_chat_user(request)
    if user.is_muted:
        raise PermissionDenied("Your account is muted in chat.")
    serializer = MessageContentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = Message.objects.create(
        room=room,
        content=serializer.validated_data["content"],
        username=user.fullname[:100],
        chat_user=user,
    )
    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


def visible_message(message_id):
    return get_object_or_404(Message, pk=message_id, room__is_active=True, hidden_at__isnull=True)


@never_cache
@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([])
@permission_classes([AllowAny])
def message_detail(request, pk):
    if request.method == "DELETE":
        return hide_chat_message(request, pk)
    message = visible_message(pk)
    if request.method == "GET":
        return Response(MessageSerializer(message).data)

    user = require_chat_user(request)
    serializer = MessageUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    values = serializer.validated_data
    if "pinned" in values:
        if not user.is_admin:
            raise PermissionDenied("Only chat moderators can pin messages.")
        message.pinned = values["pinned"]
        message.save(update_fields=["pinned", "updated_at"])
    else:
        if message.chat_user_id != user.pk or user.is_muted:
            raise PermissionDenied("Only the author can edit this message when allowed to post.")
        message.content = values["content"]
        message.edited_at = timezone.now()
        message.save(update_fields=["content", "edited_at", "updated_at"])
    return Response(MessageSerializer(message).data)


def hide_chat_message(request, message_id):
    require_chat_user(request, moderator=True)
    message = visible_message(message_id)
    message.hidden_at = timezone.now()
    message.save(update_fields=["hidden_at", "updated_at"])
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@authentication_classes([])
@permission_classes([AllowAny])
def delete_message(request, message_id):
    return hide_chat_message(request, message_id)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def flag_message(request, message_id):
    user = require_chat_user(request)
    message = visible_message(message_id)
    now = timezone.now()
    Message.objects.filter(pk=message.pk, is_reported=False).update(
        is_reported=True, reported_by=user, reported_at=now, updated_at=now
    )
    return Response({"message": "Message reported."})


@never_cache
@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def room_presence(request, room_id):
    room = get_object_or_404(ChatRoom, pk=room_id, is_active=True)
    if request.method == "POST":
        user = require_chat_user(request)
        serializer = PresenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        active = serializer.validated_data["is_online"]
        UserPresence.objects.update_or_create(
            room=room, chat_user=user,
            defaults={
                "is_online": active,
                "is_typing": active and serializer.validated_data["is_typing"],
            },
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    now = timezone.now()
    presences = UserPresence.objects.filter(
        room=room, is_online=True, last_seen__gte=now - PRESENCE_LIFETIME, chat_user__is_banned=False
    ).select_related("chat_user").order_by("pk")
    return Response([
        {
            **ChatUserSerializer(presence.chat_user).data,
            "is_typing": presence.is_typing and presence.last_seen >= now - TYPING_LIFETIME,
        }
        for presence in presences
    ])


def send_partnership_emails(partner):
    try:
        confirmation = EmailMultiAlternatives(
            "Thank you for partnering with WholeWord TV",
            "Thank you for submitting your WholeWord TV partnership request.",
            settings.DEFAULT_FROM_EMAIL, [partner.email],
        )
        confirmation.attach_alternative(render_to_string("wwt/PartnerEmail.html"), "text/html")
        confirmation.send()
    except (OSError, SMTPException, TemplateDoesNotExist):
        logger.warning("WholeWord TV could not send a partnership confirmation.")

    recipient = getattr(settings, "WWTV_PARTNERSHIP_NOTIFICATION_EMAIL", "")
    if recipient:
        try:
            send_mail(
                "New WholeWord TV partnership request",
                "A partnership request was saved. Sign in to Django admin to view it.",
                settings.DEFAULT_FROM_EMAIL, [recipient],
            )
        except (OSError, SMTPException):
            logger.warning("WholeWord TV could not send a partnership notification.")


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([PartnershipThrottle])
def submit_partnership(request):
    serializer = WholeWordPartnersSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    partner = serializer.save()
    send_partnership_emails(partner)
    return Response(
        {"message": "Partnership request submitted successfully."},
        status=status.HTTP_201_CREATED,
    )


class CurrentSeriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrentSeries.objects.order_by("pk")
    serializer_class = CurrentSeriesSerializer
    permission_classes = [AllowAny]


class NextLiveViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NextLiveSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return NextLive.objects.filter(datetime__gte=timezone.now()).order_by("datetime", "pk")

    @action(detail=False, methods=["get"])
    def next_closest(self, request):
        now = timezone.now()
        is_live = NextLive.objects.filter(datetime__gte=now - timedelta(hours=1), datetime__lte=now).exists()
        next_live = None if is_live else NextLive.objects.filter(datetime__gte=now).order_by("datetime", "pk").first()
        current_series = CurrentSeries.objects.order_by("pk").first()
        message = "We are live." if is_live else "Upcoming broadcast found" if next_live else "No upcoming broadcast"
        return Response({
            "next_live": self.get_serializer(next_live).data if next_live else None,
            "current_series": CurrentSeriesSerializer(current_series).data if current_series else None,
            "is_live": is_live,
            "message": message,
        })
