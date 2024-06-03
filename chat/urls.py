from django.urls import path
from .views import ChatRoomListCreateView, ChatRoomRetrieveUpdateDestroyView, MessageListCreateView, MessageRetrieveUpdateDestroyView

urlpatterns = [
    path('chat_rooms/', ChatRoomListCreateView.as_view(), name='chat_room_list_create'),
    path('chat_rooms/<int:pk>/', ChatRoomRetrieveUpdateDestroyView.as_view(), name='chat_room_detail'),
    path('messages/', MessageListCreateView.as_view(), name='message_list_create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message_detail'),
]
