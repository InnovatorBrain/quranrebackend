# chat/admin.py
from django.contrib import admin
from .models import ChatRoom, Message

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'created_at']
    search_fields = ['teacher__user__email', 'students__user__email']
    list_filter = ['created_at']
    ordering = ['-created_at']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_room', 'sender', 'content', 'timestamp']
    search_fields = ['sender__email', 'chat_room__teacher__user__email', 'chat_room__students__user__email']
    list_filter = ['timestamp']
    ordering = ['-timestamp']

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)
