from base64 import urlsafe_b64encode
from hashlib import sha256
from secrets import compare_digest, token_urlsafe
from time import time
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token, rotate_token
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied

from .models import ChatUsers
from .serializers import ChatUserSerializer


CHAT_SESSION_KEY = "wwtv_chat_user_id"
GOOGLE_STATE_KEY = "wwtv_google_state"
GOOGLE_STATE_MAX_AGE = 600
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def chat_user(request):
    user_id = request.session.get(CHAT_SESSION_KEY)
    if user_id is None:
        return None
    return ChatUsers.objects.filter(pk=user_id, is_banned=False).first()


def require_chat_user(request, *, moderator=False):
    SessionAuthentication().enforce_csrf(request)
    user = chat_user(request)
    if user is None:
        raise PermissionDenied("Sign in to use the chat.")
    if moderator and not user.is_admin:
        raise PermissionDenied("Only chat moderators can do that.")
    return user


def attach_chat_session(request, user):
    request.session.cycle_key()
    request.session[CHAT_SESSION_KEY] = user.pk
    rotate_token(request)


def google_enabled():
    return all(getattr(settings, key, "") for key in (
        "WWTV_FRONTEND_URL", "WWTV_GOOGLE_CLIENT_ID", "WWTV_GOOGLE_CLIENT_SECRET",
        "WWTV_GOOGLE_REDIRECT_URI",
    ))


def session_payload(request, user):
    return {
        "user": ChatUserSerializer(user).data if user else None,
        "csrf_token": get_token(request),
        "google_enabled": google_enabled(),
    }


def google_redirect(*, failed=False):
    url = settings.WWTV_FRONTEND_URL.rstrip("/") + "/"
    response = HttpResponseRedirect(url + ("?chat_auth=failed" if failed else ""))
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@require_GET
@never_cache
def google_start(request):
    if not google_enabled():
        return JsonResponse({"detail": "Google sign-in is unavailable."}, status=503)
    state = token_urlsafe(32)
    verifier = token_urlsafe(48)
    request.session[GOOGLE_STATE_KEY] = {
        "state": state,
        "verifier": verifier,
        "created_at": time(),
    }
    challenge = urlsafe_b64encode(sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    params = {
        "response_type": "code",
        "client_id": settings.WWTV_GOOGLE_CLIENT_ID,
        "redirect_uri": settings.WWTV_GOOGLE_REDIRECT_URI,
        "scope": "openid email profile",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return HttpResponseRedirect(f"{GOOGLE_AUTHORIZATION_URL}?{urlencode(params)}")


def fetch_google_profile(code, verifier):
    token_response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": verifier,
            "client_id": settings.WWTV_GOOGLE_CLIENT_ID,
            "client_secret": settings.WWTV_GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.WWTV_GOOGLE_REDIRECT_URI,
        },
        timeout=8,
        allow_redirects=False,
    )
    token_response.raise_for_status()
    token = token_response.json()["access_token"]

    profile_response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=8,
        allow_redirects=False,
    )
    profile_response.raise_for_status()
    profile = profile_response.json()
    subject, email = profile["sub"], profile["email"]
    if (
        not isinstance(subject, str) or not 0 < len(subject) <= 255
        or not isinstance(email, str) or len(email) > 254
        or profile.get("email_verified") is not True
    ):
        raise ValueError("Google did not provide a verified chat identity.")
    validate_email(email)
    return profile


@require_GET
@never_cache
def google_callback(request):
    if not google_enabled():
        return JsonResponse({"detail": "Google sign-in is unavailable."}, status=503)

    pending = request.session.get(GOOGLE_STATE_KEY)
    state = request.GET.get("state", "")
    if (
        not pending or not state.isascii()
        or not compare_digest(pending["state"], state)
        or time() - pending["created_at"] > GOOGLE_STATE_MAX_AGE
    ):
        return google_redirect(failed=True)

    request.session.pop(GOOGLE_STATE_KEY)
    code = request.GET.get("code")
    if not code or request.GET.get("error"):
        return google_redirect(failed=True)

    try:
        profile = fetch_google_profile(code, pending["verifier"])
    except (requests.RequestException, KeyError, TypeError, ValueError, ValidationError):
        return google_redirect(failed=True)

    email = profile["email"]
    name = profile.get("name")
    if not isinstance(name, str) or not name.strip():
        name = email.split("@", 1)[0]
    picture = profile.get("picture")
    if not isinstance(picture, str) or not picture.startswith("https://") or len(picture) > 2048:
        picture = None

    # Use only a subject verified by Google. The legacy profile fields could be set by guests.
    user, _ = ChatUsers.objects.get_or_create(
        google_subject=profile["sub"],
        defaults={"fullname": name.strip()[:100], "contact_email": email, "is_guest": False, "avatar_url": picture},
    )
    if user.is_banned:
        return google_redirect(failed=True)
    attach_chat_session(request, user)
    return google_redirect()
