from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.TextField()
    username = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    pinned = models.BooleanField(default=False)
    chat_user = models.ForeignKey(
        "ChatUsers", on_delete=models.CASCADE, null=True, blank=True
    )
    is_reported = models.BooleanField(default=False)
    reported_by = models.ForeignKey(
        "ChatUsers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_messages",
    )
    reported_at = models.DateTimeField(null=True, blank=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}: {self.content[:50]}"


class MessageReads(models.Model):
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="reads"
    )
    chat_user = models.ForeignKey("ChatUsers", on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("message", "chat_user")

    def __str__(self):
        return f"{self.chat_user.fullname} read {self.message.id} at {self.read_at}"


class ChatUsers(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_guest = models.BooleanField(default=True)
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    avatar_url = models.TextField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname


class UserPresence(models.Model):
    chat_user = models.ForeignKey(ChatUsers, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)
    is_typing = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("chat_user", "room")

    def __str__(self):
        return f"{self.chat_user.fullname} in {self.room.name}"


class WholeWordPartner(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "US Dollar"),
        ("NGN", "Nigerian Naira"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    partnership_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Whole Word Partner"
        verbose_name_plural = "Whole Word Partners"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class NextLive(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    datetime = models.DateTimeField()

    class Meta:
        ordering = ["-datetime"]
        verbose_name = "Next Live"
        verbose_name_plural = "Next Lives"

    def __str__(self):
        return f"{self.title} at {self.datetime}"


class CurrentSeries(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()

    class Meta:
        verbose_name = "Current Series"
        verbose_name_plural = "Current Series"

    def __str__(self):
        return f"{self.title} at {self.title}"
