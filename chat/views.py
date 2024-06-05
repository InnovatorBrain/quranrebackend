from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from django.db.models import OuterRef, Subquery, Q
from .models import User, Todo, Profile, ChatMessage
from .serializers import TodoSerializer, MessageSerializer, ProfileSerializer, UserSerializer


@api_view(['GET'])
@permission_classes([]) 
def getRoutes(request):
    routes = [
        'http://127.0.0.1:8000/chat/todo/<int:user_id>/',
        'http://127.0.0.1:8000/chat/todo-detail/<int:user_id>/<int:todo_id>/',
        'http://127.0.0.1:8000/chat/todo-mark-as-completed/<int:user_id>/<int:todo_id>/',
        'http://127.0.0.1:8000/chat/my-messages/<int:user_id>/',
        'http://127.0.0.1:8000/chat/get-messages/<int:sender_id>/<int:receiver_id>/',
        'http://127.0.0.1:8000/chat/send-messages/',
        'http://127.0.0.1:8000/chat/profile/<int:pk>/',
        'http://127.0.0.1:8000/chat/search/<str:username>/',
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulations {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulations, your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

class TodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    # queryset = Todo.objects.all()  # Add this line

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        todo = Todo.objects.filter(user=user)
        return todo

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()  # Add this line

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']
        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)
        return todo

class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()  # Add this line

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']
        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)
        todo.completed = True
        todo.save()
        return todo

class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = ChatMessage.objects.all()  # Add this line

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        messages = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user_id) |
                    Q(receiver__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user_id) |
                            Q(receiver=OuterRef('id'), sender=user_id)
                        ).order_by('-id')[:1].values_list('id', flat=True)
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
        return messages

class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = ChatMessage.objects.all()  # Add this line
    
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']
        messages = ChatMessage.objects.filter(sender__in=[sender_id, receiver_id], receiver__in=[sender_id, receiver_id])
        return messages

class SendMessages(generics.CreateAPIView):
    serializer_class = MessageSerializer
    queryset = ChatMessage.objects.all()  # Add this line

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]  

class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]  

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = Profile.objects.filter(Q(user__username__icontains=username) | Q(full_name__icontains=username) | Q(user__email__icontains=username) & 
                                       ~Q(user=logged_in_user))

        if not users.exists():
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
