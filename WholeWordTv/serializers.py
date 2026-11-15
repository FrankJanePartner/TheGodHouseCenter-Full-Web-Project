import re
from decimal import Decimal

from rest_framework import serializers

from .models import ChatRoom, ChatUsers, CurrentSeries, Message, NextLive, WholeWordPartner


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["id", "name", "is_active", "created_at", "updated_at"]


class ChatUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = ChatUsers
        fields = ["id", "fullname", "is_guest", "is_admin", "avatar_url"]

    def get_avatar_url(self, user):
        return user.avatar_url if (user.avatar_url or "").startswith("https://") else None


class GuestLoginSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=254)


class MessageSerializer(serializers.ModelSerializer):
    chat_user_id = serializers.IntegerField(read_only=True)
    room_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "content", "username", "pinned", "created_at", "updated_at",
            "room_id", "chat_user_id", "is_reported", "edited_at",
        ]


class MessageContentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)


class MessageUpdateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000, required=False)
    pinned = serializers.BooleanField(required=False)

    def validate(self, values):
        if len(values) != 1:
            raise serializers.ValidationError("Supply either message text or the pinned state.")
        return values


class PresenceSerializer(serializers.Serializer):
    is_online = serializers.BooleanField()
    is_typing = serializers.BooleanField(default=False)


class WholeWordPartnersSerializer(serializers.ModelSerializer):
    partnership_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )

    class Meta:
        model = WholeWordPartner
        fields = ["first_name", "last_name", "email", "phone_number", "currency", "partnership_amount"]

    def validate_phone_number(self, value):
        if not re.fullmatch(r"\+?[0-9(). -]+", value) or len(re.findall(r"[0-9]", value)) < 10:
            raise serializers.ValidationError("Enter a phone number containing at least 10 digits.")
        return value


class NextLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextLive
        fields = ["id", "title", "description", "datetime"]


class CurrentSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentSeries
        fields = ["id", "title", "description", "link"]
