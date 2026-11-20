from hashlib import sha256

from django.db import IntegrityError, transaction
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Moment, Registration
from .serializers import MomentSerializer, RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        email_key = sha256(email.casefold().encode("utf-8")).hexdigest() if email else None
        try:
            with transaction.atomic():
                serializer.save(registration_email_key=email_key)
        except IntegrityError:
            if email_key is None or not self.get_queryset().filter(registration_email_key=email_key).exists():
                raise
            return Response(
                {"message": "This email address already has a registration."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            {
                "message": "Your registration was received.",
                "confirmation_email_sent": False,
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
