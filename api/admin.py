from django.contrib import admin
from .models import Todo, ChatMessage

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'completed', 'date')
    list_filter = ('completed', 'date')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'recipient', 'message', 'is_read', 'date')
    list_filter = ('is_read', 'date')
    search_fields = ('message', 'user__username', 'sender__username', 'recipient__username')
    date_hierarchy = 'date'
    ordering = ('-date',)
