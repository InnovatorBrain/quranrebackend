from django.urls import path
from .views import CourseListCreateView, CourseRetrieveUpdateDestroyView, TimetableListCreateView, TimetableRetrieveUpdateDestroyView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),
    path('timetables/', TimetableListCreateView.as_view(), name='timetable-list-create'),
    path('timetables/<int:pk>/', TimetableRetrieveUpdateDestroyView.as_view(), name='timetable-detail'),
]