# Generated by Django 5.0.6 on 2024-06-03 12:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0002_rename_name_department_departmentname'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='timetables', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='course_management.department'),
        ),
        migrations.AlterField(
            model_name='course',
            name='head_of_department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses_headed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetables', to='course_management.course'),
        ),
    ]