from unittest.mock import patch

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Moment, Registration


class RegistrationAPITests(APITestCase):
    def setUp(self):
        self.url = reverse("rvc:register")
        self.payload = {
            "firstName": "Ada",
            "lastName": "Okoro",
            "email": "ada@example.test",
            "phone": "+234 801-234-5678",
            "city": "Warri",
            "churchType": "Godhouse",
            "godhouseCentre": "Warri",
            "attendanceType": "Physical",
            "accommodation": "yes",
        }

    def test_registration_persists_and_response_excludes_personal_data(self):
        with patch("django.core.mail.EmailMessage.send") as send:
            response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"message": "Your registration was received.", "confirmation_email_sent": False},
        )
        send.assert_not_called()
        registration = Registration.objects.get()
        for field, value in self.payload.items():
            self.assertEqual(getattr(registration, field), value)
        self.assertEqual(registration.otherChurch, "")

    def test_required_and_invalid_fields_return_structured_errors(self):
        response = self.client.post(
            self.url,
            {**self.payload, "firstName": "", "phone": "no digits here", "lastName": " ",
             "email": "invalid", "attendanceType": "Other", "accommodation": "maybe"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            set(response.json()["errors"]),
            {"firstName", "lastName", "phone", "email", "attendanceType", "accommodation"},
        )
        self.assertFalse(Registration.objects.exists())

    def test_church_centre_is_required_for_godhouse(self):
        response = self.client.post(self.url, {**self.payload, "godhouseCentre": " "}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("godhouseCentre", response.json()["errors"])
        self.assertFalse(Registration.objects.exists())

    def test_other_church_is_required_and_discards_stale_centre(self):
        values = {**self.payload, "churchType": "Others"}
        response = self.client.post(self.url, values, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("otherChurch", response.json()["errors"])
        self.assertFalse(Registration.objects.exists())

        response = self.client.post(self.url, {**values, "otherChurch": "Community Church"}, format="json")
        self.assertEqual(response.status_code, 201)
        registration = Registration.objects.get()
        self.assertEqual(registration.godhouseCentre, "")
        self.assertEqual(registration.otherChurch, "Community Church")

    def test_conflicting_email_keeps_original_registration(self):
        self.assertEqual(self.client.post(self.url, self.payload, format="json").status_code, 201)
        response = self.client.post(
            self.url, {**self.payload, "email": "ADA@EXAMPLE.TEST", "firstName": "Different"}, format="json"
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(set(response.json()), {"message"})
        self.assertEqual(Registration.objects.get().firstName, "Ada")

    def test_legacy_email_does_not_block_current_registration(self):
        legacy = Registration.objects.create(email=self.payload["email"])
        self.assertEqual(self.client.post(self.url, self.payload, format="json").status_code, 201)
        legacy.refresh_from_db()
        self.assertIsNone(legacy.registration_email_key)
        self.assertEqual(Registration.objects.count(), 2)

    def test_malformed_json_returns_structured_error(self):
        response = self.client.post(self.url, "{", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.json()["errors"])

    def test_no_public_registration_listing(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)


class RegistrationMigrationTests(TransactionTestCase):
    def test_adopting_legacy_tables_without_history_preserves_registrations_and_moments(self):
        app = "runningWithTheVisionConference"
        initial = [(app, "0001_initial")]
        head = [(app, "0002_registration_email_key")]
        executor = MigrationExecutor(connection)
        executor.migrate(initial)
        try:
            apps = executor.loader.project_state(initial).apps
            old_registrations = apps.get_model(app, "Registration").objects
            old_moments = apps.get_model(app, "Moment").objects
            first = old_registrations.create(email="same@example.test", firstName="First")
            second = old_registrations.create(email="same@example.test", firstName="Second")
            moment = old_moments.create(image="moments/photograph.jpg", caption="Conference", uploader="Guest")
            executor.recorder.record_unapplied(app, initial[0][1])

            MigrationExecutor(connection).migrate(head, fake_initial=True)

            self.assertEqual(
                list(Registration.objects.order_by("pk").values_list("pk", "firstName", "registration_email_key")),
                [(first.pk, "First", None), (second.pk, "Second", None)],
            )
            self.assertEqual(Moment.objects.get(pk=moment.pk).image.name, "moments/photograph.jpg")
        finally:
            MigrationExecutor(connection).migrate(head, fake_initial=True)
