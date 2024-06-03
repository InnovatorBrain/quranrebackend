from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(models.Model):
    departmentName = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    head_of_department = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
