# course_management/models.py
from django.db import models
from django.conf import settings  # Use settings to reference the custom user model

class Department(models.Model):
    departmentName = models.CharField(max_length=100)

    def __str__(self):
        return self.departmentName

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    head_of_department = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="courses_headed"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.name

class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="timetables")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="timetables")
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course.name} - {self.day} - {self.start_time} to {self.end_time}"
