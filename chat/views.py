from rest_framework import generics
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from .permissions import IsTeacherOrStudent

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    # permission_classes = [IsTeacherOrStudent]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return ChatRoom.objects.filter(teacher=user)
        elif user.is_student:
            return ChatRoom.objects.filter(students=user)
        return ChatRoom.objects.none()

class ChatRoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    # permission_classes = [IsTeacherOrStudent]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return ChatRoom.objects.filter(teacher=user)
        elif user.is_student:
            return ChatRoom.objects.filter(students=user)
        return ChatRoom.objects.none()

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = [IsTeacherOrStudent]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(chat_room__teacher=user) | Message.objects.filter(chat_room__students=user)

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = [IsTeacherOrStudent]
