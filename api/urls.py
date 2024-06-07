from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.testEndPoint, name='test'),
    path('', views.getRoutes),

    # Todo URLs
    path("todo/<int:user_id>/", views.TodoListView.as_view()),
    path("todo-detail/<int:user_id>/<int:todo_id>/", views.TodoDetailView.as_view()),
    path("todo-mark-as-completed/<int:user_id>/<int:todo_id>/", views.TodoMarkAsCompleted.as_view()),

    # Chat/Text Messaging Functionality
    path("my-messages/<int:user_id>/", views.MyInbox.as_view()),
    path("get-messages/<int:sender_id>/<int:recipient_id>/", views.GetMessages.as_view()),
    path("send-messages/", views.SendMessages.as_view()),

    # Profile URLs
    path("profile/<int:pk>/", views.ProfileDetail.as_view()),
    path("search/<str:username>/", views.SearchUser.as_view()),
]
