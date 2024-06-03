from django.contrib import admin
from django import forms
from .models import Department, Course, Timetable

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs['disabled'] = True  # Disable the field to prevent modification

    def label_from_instance(self, obj):
        return obj.departmentName  # Display the department name instead of "objects"

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "departmentName"]
    search_fields = ["departmentName"]
    list_per_page = 10
    
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ["id", "name", "description", "get_department_name"]
    list_filter = [("department", admin.RelatedOnlyFieldListFilter)]
    search_fields = ["name", "description"]
    list_per_page = 10

    def get_department_name(self, obj):
        return obj.department.departmentName if obj.department else "-"
    get_department_name.short_description = "Department"

class TimetableAdmin(admin.ModelAdmin):
    list_display = ["id", "get_course_name", "day", "start_time", "end_time"]
    list_filter = ["course__name", "day"]
    search_fields = ["course__name"]
    list_per_page = 10

    def get_course_name(self, obj):
        return obj.course.name if obj.course else "-"
    get_course_name.short_description = "Course"

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Timetable, TimetableAdmin)
