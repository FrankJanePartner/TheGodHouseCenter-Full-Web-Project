from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    ChatRoom,
    Message,
    WholeWordPartner,
    NextLive,
    CurrentSeries,
    ChatUsers,
    MessageReads,
    UserPresence,
)
from .serializers import (
    WholeWordPartnersSerializer,
    NextLiveSerializer,
    CurrentSeriesSerializer,
    ChatRoomSerializer,
    MessageSerializer,
    ChatUsersSerializer,
    MessageReadsSerializer,
    UserPresenceSerializer,
)
from rest_framework.response import Response as DRFResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template import loader
from rest_framework import filters
from typing import Any
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def guest_login(request):
    """Register guest user and return Token"""
    try:
        username = request.data.get("username")
        email = request.data.get("email")

        if not username or not email:
            return Response(
                {"error": "Username and email are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if user exists
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "first_name": username,
                "password": None,  # no password for guest
            },
        )

        # Get or create token
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])  # AllowAny for GET, IsAdminUser for POST
def chat_status(request):
    """Get or set chat status"""
    try:
        room, created = ChatRoom.objects.get_or_create(name="Main Chat")

        if request.method == "GET":
            return Response({"is_on": room.is_active, "room_id": room.id})

        elif request.method == "POST":
            # Only authenticated users (admins) should be able to change status
            if not request.user.is_authenticated or not request.user.is_staff:
                return Response(
                    {"error": "Authentication required to change chat status"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            new_status = request.data.get("is_on")
            if new_status is None:
                return Response(
                    {"error": "'is_on' parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            room.is_active = new_status
            room.save()

            if not new_status:  # If chat is being turned off, wipe messages
                Message.objects.filter(room=room).delete()

            return Response(
                {
                    "is_on": room.is_active,
                    "room_id": room.id,
                    "message": "Chat status updated",
                }
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current user info"""
    return Response(
        {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        }
    )


# Chat Room List/Detail Views
@api_view(["GET"])
@permission_classes([AllowAny])
def ChatRoomList(request):
    """List all chat rooms"""
    rooms = ChatRoom.objects.all()
    serializer = ChatRoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def ChatRoomDetail(request, pk):
    """Get specific chat room"""
    try:
        room = ChatRoom.objects.get(pk=pk)
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)
    except ChatRoom.DoesNotExist:
        return Response(
            {"error": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND
        )


# Chat Message Views
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def ChatMessageList(request, room_id):
    """List messages for a room or create a new message"""
    try:
        room = ChatRoom.objects.get(pk=room_id)

        if request.method == "GET":
            messages = Message.objects.filter(room=room).order_by("created_at")
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            content = request.data.get("content")
            username = request.data.get(
                "username", "Anonymous"
            )  # Use provided username

            if not content:
                return Response(
                    {"error": "Message content is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            message = Message.objects.create(
                room=room,
                content=content,
                username=username,
                user=None,  # Do not link to Django User object
            )
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ChatRoom.DoesNotExist:
        return Response(
            {"error": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def ChatMessageDetail(request, pk):
    """Get specific message"""
    try:
        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    except Message.DoesNotExist:
        return Response(
            {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    """Delete a message"""
    return Response({"message": "Message deleted successfully"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def flag_message(request, message_id):
    """Flag a message"""
    return Response({"message": "Message flagged successfully"})


class WholeWordPartnerViewSet(viewsets.ModelViewSet):
    queryset = WholeWordPartner.objects.all()
    serializer_class = WholeWordPartnersSerializer

    @action(detail=False, methods=["post"])
    def submit(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            partner = serializer.save()

            # Send email to user with HTML template
            user_email = partner.email
            subject = "Thank you for partnering with WholeWord TV"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [user_email]
            html_content = loader.render_to_string("wwt/PartnerEmail.html")
            msg = EmailMultiAlternatives(subject, "", from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

            # Send email to admin(s)
            admin_emails = ["info.godhouse@gmail.com"]
            send_mail(
                "New Partnership Request",
                f"""New partner: {partner.first_name} {partner.last_name}, \n
                Email: {partner.email}\n
                Phone Number: {partner.phone_number}\n
                partnership Amount: {partner.currency}{partner.partnership_amount}\n""",
                settings.DEFAULT_FROM_EMAIL,
                admin_emails,
                fail_silently=True,
            )

            return Response(
                {"message": "Partnership request submitted successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentSeriesViewSet(viewsets.ModelViewSet):
    queryset = CurrentSeries.objects.all()
    serializer_class = CurrentSeriesSerializer


class NextLiveViewSet(viewsets.ModelViewSet):
    serializer_class = NextLiveSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["datetime"]
    ordering = ["datetime"]

    def get_queryset(self) -> Any:
        now = timezone.now()
        return NextLive.objects.filter(datetime__gte=now).order_by("datetime")

    # Additional action to get the next closest live service
    @action(detail=False, methods=["get"])
    def next_closest(self, request: Request) -> DRFResponse:
        now = timezone.now()
        one_hour_ago = now - timezone.timedelta(hours=1)

        # Check for a live stream that started in the last hour
        live_stream = (
            NextLive.objects.filter(datetime__gte=one_hour_ago, datetime__lte=now)
            .order_by("-datetime")
            .first()
        )

        current_series = CurrentSeries.objects.first()
        current_series_data = (
            CurrentSeriesSerializer(current_series).data if current_series else None
        )

        if live_stream:
            return DRFResponse(
                {
                    "next_live": None,
                    "current_series": current_series_data,
                    "message": "🚀🎉 WE ARE LIVE!!! 🎉🚀",
                }
            )

        next_live = (
            NextLive.objects.filter(datetime__gte=now).order_by("datetime").first()
        )

        response_data = {
            "next_live": None,
            "current_series": current_series_data,
            "message": "No upcoming broadcast",
        }

        if next_live:
            serializer = self.get_serializer(next_live)
            response_data["next_live"] = serializer.data
            response_data["message"] = "Upcoming broadcast found"

        return DRFResponse(response_data)


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatUsersViewSet(viewsets.ModelViewSet):
    queryset = ChatUsers.objects.all()
    serializer_class = ChatUsersSerializer


class MessageReadsViewSet(viewsets.ModelViewSet):
    queryset = MessageReads.objects.all()
    serializer_class = MessageReadsSerializer


class UserPresenceViewSet(viewsets.ModelViewSet):
    queryset = UserPresence.objects.all()
    serializer_class = UserPresenceSerializer
