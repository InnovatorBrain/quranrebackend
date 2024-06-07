from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import OuterRef, Subquery

from auth_account.models import CustomUser
from .models import Todo, ChatMessage
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, TodoSerializer, ChatMessageSerializer, ProfileSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = CustomUser.objects.get(id=user_id)
        return Todo.objects.filter(user=user)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']
        user = CustomUser.objects.get(id=user_id)
        return Todo.objects.get(id=todo_id, user=user)

class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']
        user = CustomUser.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)
        todo.completed = True
        todo.save()
        return todo

class MyInbox(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        messages = ChatMessage.objects.filter(
            id__in=Subquery(
                ChatMessage.objects.filter(
                    Q(sender__recipient=user_id) |
                    Q(recipient__sender=user_id)
                ).order_by('-id')[:1].values_list('id', flat=True)
            )
        ).order_by("-id")
        return messages

class GetMessages(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        recipient_id = self.kwargs['recipient_id']
        return ChatMessage.objects.filter(sender__in=[sender_id, recipient_id], recipient__in=[sender_id, recipient_id])

class SendMessages(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = CustomUser.objects.filter(
            Q(username__icontains=username) | Q(email__icontains=username)
        ).exclude(id=logged_in_user.id)

        if not users.exists():
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
