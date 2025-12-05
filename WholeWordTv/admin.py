from django.contrib import admin
from .models import WholeWordPartner, NextLive, CurrentSeries, ChatRoom, Message, MessageReads, ChatUsers

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('-updated_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'username', 'pinned', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'username')
    ordering = ('-created_at',)


admin.site.register(WholeWordPartner)
admin.site.register(NextLive)
admin.site.register(CurrentSeries)
admin.site.register(ChatUsers)