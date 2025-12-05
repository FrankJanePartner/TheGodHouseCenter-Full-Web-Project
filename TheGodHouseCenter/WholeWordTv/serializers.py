from rest_framework import serializers
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


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["id", "name", "is_active"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "content",
            "username",
            "pinned",
            "created_at",
            "updated_at",
            "room",
            "user",
            "chat_user",
            "is_reported",
            "reported_by",
            "reported_at",
            "edited_at",
        ]


class WholeWordPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WholeWordPartner
        fields = "__all__"


class NextLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextLive
        fields = "__all__"


# class ChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chat
#         fields = '__all__'


class CurrentSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentSeries
        fields = "__all__"


class ChatUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUsers
        fields = "__all__"


class MessageReadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReads
        fields = "__all__"


class UserPresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPresence
        fields = "__all__"
