from rest_framework import serializers
from .models import ChatRoom, Message
from auth_account.models import StudentProfile, TeacherProfile

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'content', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    students = serializers.SlugRelatedField(
        queryset=StudentProfile.objects.all(), slug_field='user__email', many=True
    )

    class Meta:
        model = ChatRoom
        fields = ['id', 'teacher', 'students', 'created_at', 'messages']
