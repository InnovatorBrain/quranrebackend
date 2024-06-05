from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.testEndPoint, name='test'),
    path('', views.getRoutes, name='routes'),
    path("todo/<int:user_id>/", views.TodoListView.as_view(), name='todo_list'),
    path("todo-detail/<int:user_id>/<int:todo_id>/", views.TodoDetailView.as_view(), name='todo_detail'),
    path("todo-mark-as-completed/<int:user_id>/<int:todo_id>/", views.TodoMarkAsCompleted.as_view(), name='todo_mark_completed'),
    path("my-messages/<int:user_id>/", views.MyInbox.as_view(), name='my_messages'),
    path("get-messages/<int:sender_id>/<int:receiver_id>/", views.GetMessages.as_view(), name='get_messages'),
    path("send-messages/", views.SendMessages.as_view(), name='send_messages'),
    path("profile/<int:pk>/", views.ProfileDetail.as_view(), name='profile_detail'),
    path("search/<str:username>/", views.SearchUser.as_view(), name='search_user'),
]
