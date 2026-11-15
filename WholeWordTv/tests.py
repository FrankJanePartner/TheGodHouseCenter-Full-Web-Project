from datetime import timedelta
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlsplit

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase

from .models import ChatRoom, ChatUsers, CurrentSeries, Message, NextLive, UserPresence, WholeWordPartner


def url(name, *args):
    return reverse(f"whole-word-tv:{name}", args=args)


class ChatTests(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.room = ChatRoom.objects.create(name="Main Chat")

    def csrf(self):
        return self.client.get(url("current-user")).json()["csrf_token"]

    def guest(self, name, email):
        return self.client.post(
            url("guest"),
            {"fullname": name, "email": email},
            format="json",
            HTTP_X_CSRFTOKEN=self.csrf(),
        )

    def send_message(self, payload):
        return self.client.post(
            url("chatmessage-list", self.room.pk),
            payload,
            format="json",
            HTTP_X_CSRFTOKEN=self.csrf(),
        )

    def test_guest_session_requires_csrf_and_cannot_claim_a_privileged_profile(self):
        church_admin = get_user_model().objects.create_user(
            username="church-admin", email="leader@example.test", is_staff=True
        )
        old_profile = ChatUsers.objects.create(
            fullname="Admin", email=church_admin.email, is_guest=False, is_admin=True
        )
        untrusted = self.client.post(
            url("guest"), {"fullname": "Visitor", "email": church_admin.email}, format="json"
        )
        self.assertEqual(untrusted.status_code, 403)

        response = self.guest("Visitor", church_admin.email)
        self.assertEqual(response.status_code, 201)
        profile = response.json()["user"]
        self.assertNotEqual(profile["id"], old_profile.pk)
        self.assertTrue(profile["is_guest"])
        self.assertFalse(profile["is_admin"])
        self.assertNotIn("email", profile)
        self.assertNotIn("token", response.json())
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertTrue(response.cookies[settings.SESSION_COOKIE_NAME]["httponly"])

    def test_cross_origin_session_write_needs_a_trusted_origin_and_csrf_token(self):
        frontend_origin = "https://wholewordtv.godhouse.org"
        preflight = self.client.options(
            url("guest"), HTTP_ORIGIN=frontend_origin, HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
        )
        self.assertEqual(preflight.headers.get("Access-Control-Allow-Origin"), frontend_origin)
        self.assertEqual(preflight.headers.get("Access-Control-Allow-Credentials"), "true")
        credentials = {"fullname": "Visitor", "email": "visitor@example.test"}
        token = self.csrf()
        denied = self.client.post(
            url("guest"), credentials, secure=True, format="json", HTTP_X_CSRFTOKEN=token,
            HTTP_ORIGIN="https://other.example.test",
        )
        self.assertEqual(denied.status_code, 403)
        accepted = self.client.post(
            url("guest"), credentials, secure=True, format="json", HTTP_X_CSRFTOKEN=token,
            HTTP_ORIGIN=frontend_origin,
        )
        self.assertEqual(accepted.status_code, 201)

    def test_messages_use_session_author_and_only_owner_edits(self):
        guest_id = self.guest("Visitor A", "a@example.test").json()["user"]["id"]
        response = self.send_message(
            {"content": "Hello chat", "username": "Spoofed", "chat_user_id": 999, "pinned": True}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["chat_user_id"], guest_id)
        self.assertEqual(response.json()["username"], "Visitor A")
        self.assertFalse(response.json()["pinned"])

        detail = url("chatmessage-detail", response.json()["id"])
        denied = self.client.patch(detail, {"pinned": True}, format="json", HTTP_X_CSRFTOKEN=self.csrf())
        self.assertEqual(denied.status_code, 403)

        edited = self.client.patch(
            detail, {"content": "Edited greeting"}, format="json", HTTP_X_CSRFTOKEN=self.csrf()
        )
        self.assertEqual(edited.status_code, 200)
        self.assertIsNotNone(edited.json()["edited_at"])
        self.assertEqual(edited.json()["content"], "Edited greeting")

        self.client.post(url("logout"), {}, format="json", HTTP_X_CSRFTOKEN=self.csrf())
        self.assertIsNone(self.client.get(url("current-user")).json()["user"])
        self.guest("Visitor B", "b@example.test")
        rejected = self.client.patch(
            detail, {"content": "Not mine"}, format="json", HTTP_X_CSRFTOKEN=self.csrf()
        )
        self.assertEqual(rejected.status_code, 403)
        self.assertEqual(Message.objects.get().content, "Edited greeting")

    def test_moderator_can_pin_and_hide_without_deleting_record(self):
        self.guest("Visitor", "visitor@example.test")
        message = self.send_message({"content": "Test message"}).json()
        self.assertEqual(
            self.client.post(
                url("flag-message", message["id"]), {}, format="json", HTTP_X_CSRFTOKEN=self.csrf()
            ).status_code,
            200,
        )
        ChatUsers.objects.filter(pk=message["chat_user_id"]).update(is_admin=True)
        detail = url("chatmessage-detail", message["id"])
        pinned = self.client.patch(detail, {"pinned": True}, format="json", HTTP_X_CSRFTOKEN=self.csrf())
        self.assertTrue(pinned.json()["pinned"])
        self.assertTrue(pinned.json()["is_reported"])
        self.assertNotIn("reported_by", pinned.json())
        self.assertEqual(
            self.client.delete(url("delete-message", message["id"]), HTTP_X_CSRFTOKEN=self.csrf()).status_code,
            204,
        )
        self.assertTrue(Message.objects.filter(pk=message["id"]).exists())
        self.assertEqual(self.client.get(url("chatmessage-list", self.room.pk)).json(), [])

    def test_closed_room_keeps_records_and_stops_showing_the_feed(self):
        Message.objects.create(room=self.room, username="Historic sender", content="Stored chat")
        self.room.is_active = False
        self.room.save()
        self.assertEqual(self.client.get(url("chat-status")).json(), {"is_on": False, "room_id": None})
        self.assertEqual(self.client.get(url("chatmessage-list", self.room.pk)).status_code, 404)
        self.assertEqual(Message.objects.count(), 1)

    def test_presence_requires_session_and_omits_email_and_stale_profiles(self):
        presence_url = url("chat-presence", self.room.pk)
        self.assertEqual(
            self.client.post(
                presence_url, {"is_online": True}, format="json", HTTP_X_CSRFTOKEN=self.csrf()
            ).status_code,
            403,
        )
        self.guest("Visitor", "visitor@example.test")
        response = self.client.post(
            presence_url, {"is_online": True, "is_typing": True}, format="json", HTTP_X_CSRFTOKEN=self.csrf()
        )
        self.assertEqual(response.status_code, 204)
        visible = self.client.get(presence_url).json()[0]
        self.assertEqual(visible["fullname"], "Visitor")
        self.assertTrue(visible["is_typing"])
        self.assertNotIn("email", visible)
        UserPresence.objects.update(last_seen=timezone.now() - timedelta(minutes=5))
        self.assertEqual(self.client.get(presence_url).json(), [])

    def test_muted_and_banned_users_cannot_send(self):
        user_id = self.guest("Visitor", "visitor@example.test").json()["user"]["id"]
        ChatUsers.objects.filter(pk=user_id).update(is_muted=True)
        self.assertEqual(self.send_message({"content": "Muted"}).status_code, 403)
        ChatUsers.objects.filter(pk=user_id).update(is_muted=False, is_banned=True)
        self.assertEqual(self.send_message({"content": "Banned"}).status_code, 403)
        self.assertIsNone(self.client.get(url("current-user")).json()["user"])
        self.assertFalse(Message.objects.exists())


@override_settings(
    WWTV_FRONTEND_URL="https://wholewordtv.godhouse.org",
    WWTV_GOOGLE_CLIENT_ID="local-test-client",
    WWTV_GOOGLE_CLIENT_SECRET="local-test-secret",
    WWTV_GOOGLE_REDIRECT_URI="https://godhouse.org/api/whole-word-tv/auth/google/callback/",
)
class GoogleChatTests(APITestCase):
    def start(self):
        response = self.client.get(url("google-start"))
        self.assertEqual(response.status_code, 302)
        params = parse_qs(urlsplit(response["Location"]).query)
        self.assertEqual(params["client_id"], ["local-test-client"])
        self.assertNotIn("local-test-secret", response["Location"])
        return params["state"][0]

    @patch("WholeWordTv.chat_auth.requests.post")
    def test_mismatched_state_never_exchanges_code(self, exchange):
        self.start()
        response = self.client.get(url("google-callback"), {"state": "wrong", "code": "authorization"})
        self.assertEqual(response["Location"], "https://wholewordtv.godhouse.org/?chat_auth=failed")
        exchange.assert_not_called()
        self.assertIsNone(self.client.get(url("current-user")).json()["user"])

    @patch("WholeWordTv.chat_auth.requests.get")
    @patch("WholeWordTv.chat_auth.requests.post")
    def test_verified_google_subject_creates_session_without_reusing_email(self, exchange, userinfo):
        old_profile = ChatUsers.objects.create(fullname="Admin", email="leader@example.test", is_admin=True)
        exchange.return_value = Mock(json=lambda: {"access_token": "test-token"})
        userinfo.return_value = Mock(json=lambda: {
            "sub": "verified-subject",
            "name": "Verified viewer",
            "email": old_profile.email,
            "email_verified": True,
        })

        state = self.start()
        response = self.client.get(url("google-callback"), {"state": state, "code": "authorization"})
        self.assertEqual(response["Location"], "https://wholewordtv.godhouse.org/")
        profile = self.client.get(url("current-user")).json()["user"]
        self.assertNotEqual(profile["id"], old_profile.pk)
        self.assertFalse(profile["is_guest"])
        self.assertFalse(profile["is_admin"])
        self.assertEqual(profile["fullname"], "Verified viewer")

        replay = self.client.get(url("google-callback"), {"state": state, "code": "authorization"})
        self.assertEqual(replay["Location"], "https://wholewordtv.godhouse.org/?chat_auth=failed")
        self.assertEqual(exchange.call_count, 1)

        state = self.start()
        self.client.get(url("google-callback"), {"state": state, "code": "next-authorization"})
        self.assertEqual(self.client.get(url("current-user")).json()["user"]["id"], profile["id"])
        self.assertEqual(ChatUsers.objects.count(), 2)

    @patch("WholeWordTv.chat_auth.requests.get")
    @patch("WholeWordTv.chat_auth.requests.post")
    def test_unverified_google_email_cannot_sign_in(self, exchange, userinfo):
        exchange.return_value = Mock(json=lambda: {"access_token": "test-token"})
        userinfo.return_value = Mock(json=lambda: {
            "sub": "subject", "email": "unverified@example.test", "email_verified": False,
        })
        response = self.client.get(
            url("google-callback"), {"state": self.start(), "code": "authorization"},
        )
        self.assertEqual(response["Location"], "https://wholewordtv.godhouse.org/?chat_auth=failed")
        self.assertIsNone(self.client.get(url("current-user")).json()["user"])
        self.assertFalse(ChatUsers.objects.exists())


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PublicContentTests(APITestCase):
    def test_public_partnership_submit_saves_but_does_not_list_private_records(self):
        data = {
            "first_name": "First", "last_name": "Last", "email": "partner@example.test",
            "phone_number": "+2348001112233", "currency": "NGN", "partnership_amount": "5000.00",
        }
        self.assertEqual(self.client.post(url("wholewordpartners-submit"), data, format="json").status_code, 201)
        self.assertEqual(WholeWordPartner.objects.get().email, data["email"])
        self.assertEqual(mail.outbox[0].to, [data["email"]])
        self.assertEqual(self.client.get(url("wholewordpartners-list")).status_code, 405)

    def test_partner_amount_must_be_positive(self):
        response = self.client.post(url("wholewordpartners-submit"), {"partnership_amount": "0.00"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("partnership_amount", response.json())
        self.assertFalse(WholeWordPartner.objects.exists())

    def test_schedule_and_series_are_read_only_and_choose_next_broadcast(self):
        now = timezone.now()
        for hours in [2, 1, -5]:
            NextLive.objects.create(title=f"Scheduled {hours}", description="Service", datetime=now + timedelta(hours=hours))
        series = CurrentSeries.objects.create(title="Series", link="https://example.test", description="Teaching")
        response = self.client.get(url("nextlive-next-closest"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["next_live"]["title"], "Scheduled 1")
        self.assertEqual(response.json()["current_series"]["id"], series.pk)
        self.assertFalse(response.json()["is_live"])
        self.assertEqual(self.client.post(url("currentseries-list"), {}, format="json").status_code, 405)


class WholeWordTvMigrationTests(TransactionTestCase):
    def test_adopting_all_legacy_tables_preserves_records_and_old_provider_ids(self):
        app = "WholeWordTv"
        initial = [(app, "0001_initial")]
        current = [(app, "0002_django_chat_sessions")]
        executor = MigrationExecutor(connection)
        executor.migrate(initial)
        try:
            apps = executor.loader.project_state(initial).apps
            room = apps.get_model(app, "ChatRoom").objects.create(name="Main Chat")
            user = apps.get_model(app, "ChatUsers").objects.create(
                fullname="Historic user", email="historic@example.test", google_id="legacy-provider-id",
                is_admin=True,
            )
            message = apps.get_model(app, "Message").objects.create(
                room=room, chat_user=user, username=user.fullname, content="Historic message",
            )
            partner = apps.get_model(app, "WholeWordPartner").objects.create(
                first_name="First", last_name="Last", email="historic-partner@example.test",
                phone_number="08012345678", currency="NGN", partnership_amount="1000",
            )
            executor.recorder.record_unapplied(app, "0001_initial")

            MigrationExecutor(connection).migrate(current, fake_initial=True)

            historic_user = ChatUsers.objects.get(pk=user.pk)
            self.assertEqual(historic_user.email, user.email)
            self.assertEqual(historic_user.google_id, user.google_id)
            self.assertIsNone(historic_user.google_subject)
            self.assertTrue(historic_user.is_admin)
            historic_message = Message.objects.get(pk=message.pk)
            self.assertEqual(historic_message.chat_user_id, user.pk)
            self.assertEqual(historic_message.content, "Historic message")
            self.assertIsNone(historic_message.hidden_at)
            self.assertEqual(WholeWordPartner.objects.get(pk=partner.pk).email, partner.email)
        finally:
            MigrationExecutor(connection).migrate(current, fake_initial=True)
