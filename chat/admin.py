from django.contrib import admin
from .models import User, Profile, Todo, ChatMessage

class TodoAdmin(admin.ModelAdmin):
    list_editable = ['completed']
    list_display = ['user', 'title', 'completed', 'date']

class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read', 'message']
    list_display = ['user', 'sender', 'receiver', 'is_read', 'message']

admin.site.register(Todo, TodoAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
