from django.contrib import admin
from django.utils import timezone

from .models import ChatRoom, ChatUsers, CurrentSeries, Message, NextLive, WholeWordPartner

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('-updated_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'username', 'pinned', 'is_reported', 'hidden_at', 'content', 'created_at')
    list_filter = ('room', 'pinned', 'is_reported', 'hidden_at', 'created_at')
    search_fields = ('content', 'username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'edited_at', 'reported_by', 'reported_at', 'hidden_at')
    actions = ('hide_messages', 'restore_messages')

    @admin.action(permissions=['change'], description='Hide selected messages from the public chat')
    def hide_messages(self, request, queryset):
        now = timezone.now()
        queryset.filter(hidden_at__isnull=True).update(hidden_at=now, updated_at=now)

    @admin.action(permissions=['change'], description='Restore selected messages to the public chat')
    def restore_messages(self, request, queryset):
        queryset.exclude(hidden_at__isnull=True).update(hidden_at=None, updated_at=timezone.now())


@admin.register(ChatUsers)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'contact_email', 'is_guest', 'is_admin', 'is_muted', 'is_banned')
    list_filter = ('is_guest', 'is_admin', 'is_muted', 'is_banned')
    search_fields = ('fullname', 'contact_email', 'email')
    readonly_fields = ('email', 'google_id', 'google_subject', 'created_at', 'updated_at')


@admin.register(WholeWordPartner)
class WholeWordPartnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'currency', 'partnership_amount')
    list_filter = ('currency',)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')


@admin.register(NextLive)
class NextLiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime')
    search_fields = ('title',)


@admin.register(CurrentSeries)
class CurrentSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')
    search_fields = ('title',)
