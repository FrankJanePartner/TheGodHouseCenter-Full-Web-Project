from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Registration, Moment
from .serializers import RegistrationSerializer, MomentSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class RegistrationView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()

        # If email exists, send HTML email
        if instance.email:
            context = {
                "firstName": instance.firstName,
                "lastName": instance.lastName,
                "email": instance.email,
                "city": instance.city,
                "attendanceType": instance.attendanceType,
            }

            html_message = render_to_string("rvc/rvc-email.html", context)

            email = EmailMessage(
                subject="Your RVC Registration Confirmation",
                body=html_message,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                to=[instance.email],
            )

            email.content_subtype = "html"  # Important for HTML rendering
            email.send()

class MomentUploadView(generics.CreateAPIView):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer
    parser_classes = [MultiPartParser, FormParser]


class MomentListView(generics.ListAPIView):
    queryset = Moment.objects.order_by("-created_at")
    serializer_class = MomentSerializer
    