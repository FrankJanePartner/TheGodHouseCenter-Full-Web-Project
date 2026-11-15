from unittest.mock import patch

from django.http import HttpResponse
from django.test import TestCase, override_settings


@override_settings(HOMEPAGE_REDIRECT_URL="https://maintain.godhouse.org/")
class HomepageMaintenanceTests(TestCase):
    def test_only_the_homepage_redirects(self):
        response = self.client.get("/")
        self.assertRedirects(response, "https://maintain.godhouse.org/", fetch_redirect_response=False)
        self.assertIn("no-store", response["Cache-Control"])

        self.assertEqual(self.client.get("/api/whole-word-tv/chat/status/").status_code, 200)
        self.assertEqual(self.client.get("/api/rvc/register/").status_code, 405)
        self.assertRedirects(self.client.get("/admin/"), "/admin/login/?next=/admin/", fetch_redirect_response=False)

    @override_settings(HOMEPAGE_REDIRECT_URL="")
    @patch("core.views.render", return_value=HttpResponse("Church homepage"))
    def test_clearing_the_setting_restores_the_homepage(self, render_home):
        self.assertContains(self.client.get("/"), "Church homepage")
        self.assertEqual(render_home.call_args.args[1], "core/home.html")
