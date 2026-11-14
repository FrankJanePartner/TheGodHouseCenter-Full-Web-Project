import logging
from hashlib import sha256

from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Moment, Registration
from .serializers import MomentSerializer, RegistrationSerializer


logger = logging.getLogger(__name__)


def _send_registration_confirmation(registration):
    try:
        html = render_to_string("rvc/rvc-email.html", {"first_name": registration.firstName})
        sent = send_mail(
            subject="Registration Confirmed: You're RVC-bound!",
            message=(
                f"Hello {registration.firstName},\n\n"
                "Congratulations, you are RVC-bound! Your registration for Running with the Vision "
                "Conference 2026 is confirmed.\n\n"
                "Visit https://rvc.godhouse.org for conference details. For questions or "
                "accommodation enquiries, email rvc@godhouse.org.\n\n"
                "See you soon,\nThe Godhouse Missions International"
            ),
            from_email=None,
            recipient_list=[registration.email],
            html_message=html,
        )
        return sent == 1
    except Exception as error:
        # Mail failures must not change the outcome of an already saved registration.
        logger.warning("RVC confirmation failed for registration %s (%s)", registration.pk, type(error).__name__)
        return False


class RegistrationView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_key = sha256(serializer.validated_data["email"].casefold().encode("utf-8")).hexdigest()
        try:
            with transaction.atomic():
                registration = serializer.save(registration_email_key=email_key)
        except IntegrityError:
            if not self.get_queryset().filter(registration_email_key=email_key).exists():
                raise
            return Response(
                {"message": "This email address already has a registration."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            {
                "message": "Your registration was received.",
                "confirmation_email_sent": _send_registration_confirmation(registration),
            },
            status=status.HTTP_201_CREATED,
        )

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            errors = (
                response.data
                if isinstance(exc, ValidationError)
                else {"non_field_errors": [response.data.get("detail", "Invalid request.")]}
            )
            response.data = {"message": "Please check your registration details.", "errors": errors}
        return response


class MomentUploadView(generics.CreateAPIView):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer
    parser_classes = [MultiPartParser, FormParser]


class MomentListView(generics.ListAPIView):
    queryset = Moment.objects.order_by("-created_at")
    serializer_class = MomentSerializer
