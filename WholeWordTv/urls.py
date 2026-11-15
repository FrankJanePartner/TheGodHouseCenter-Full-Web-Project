from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import chat_auth, views


app_name = "whole-word-tv"
router = DefaultRouter()
router.register("nextlive", views.NextLiveViewSet, basename="nextlive")
router.register("currentseries", views.CurrentSeriesViewSet, basename="currentseries")

urlpatterns = [
    path("chat/status/", views.chat_status, name="chat-status"),
    path("chatrooms/", views.chat_room_list, name="chatroom-list"),
    path("chatrooms/<int:pk>/", views.chat_room_detail, name="chatroom-detail"),
    path("chatrooms/<int:room_id>/messages/", views.room_messages, name="chatmessage-list"),
    path("chatrooms/<int:room_id>/presence/", views.room_presence, name="chat-presence"),
    path("messages/<int:pk>/", views.message_detail, name="chatmessage-detail"),
    path("messages/<int:message_id>/delete/", views.delete_message, name="delete-message"),
    path("messages/<int:message_id>/flag/", views.flag_message, name="flag-message"),
    path("user/current/", views.current_user, name="current-user"),
    path("user/logout/", views.logout, name="logout"),
    path("api/guest/", views.guest_login, name="guest"),
    path("auth/google/", chat_auth.google_start, name="google-start"),
    path("auth/google/callback/", chat_auth.google_callback, name="google-callback"),
    path("wholewordpartners/", views.submit_partnership, name="wholewordpartners-list"),
    path("wholewordpartners/submit/", views.submit_partnership, name="wholewordpartners-submit"),
    path("", include(router.urls)),
]
