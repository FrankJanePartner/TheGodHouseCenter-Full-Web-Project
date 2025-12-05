app_name = "whole-word-tv"

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WholeWordPartnerViewSet,
    NextLiveViewSet,
    CurrentSeriesViewSet,
    ChatRoomViewSet,
    MessageViewSet,
    ChatUsersViewSet,
    MessageReadsViewSet,
    UserPresenceViewSet,
    chat_status,
    ChatRoomList,
    ChatRoomDetail,
    ChatMessageList,
    ChatMessageDetail,
    delete_message,
    flag_message,
    current_user,
    guest_login,
)

router = DefaultRouter()
router.register(
    r"wholewordpartners", WholeWordPartnerViewSet, basename="wholewordpartners"
)
router.register(r"nextlive", NextLiveViewSet, basename="nextlive")
router.register(r"currentseries", CurrentSeriesViewSet, basename="currentseries")
router.register(r"chatrooms", ChatRoomViewSet, basename="chatrooms")
router.register(r"messages", MessageViewSet, basename="messages")
router.register(r"chatusers", ChatUsersViewSet, basename="chatusers")
router.register(r"messagereads", MessageReadsViewSet, basename="messagereads")
router.register(r"userpresence", UserPresenceViewSet, basename="userpresence")

urlpatterns = [
    path("chatrooms/", ChatRoomList, name="chatroom-list"),
    path("chatrooms/<int:pk>/", ChatRoomDetail, name="chatroom-detail"),
    path("chatrooms/<int:room_id>/messages/", ChatMessageList, name="chatmessage-list"),
    path("messages/<int:pk>/", ChatMessageDetail, name="chatmessage-detail"),
    path("messages/<int:message_id>/delete/", delete_message, name="delete-message"),
    path("messages/<int:message_id>/flag/", flag_message, name="flag-message"),
    path("user/current/", current_user, name="current-user"),
    path("api/guest/", guest_login, name="guest"),
    path("", include(router.urls)),
    path("chat/status/", chat_status, name="chat-status"),
]
