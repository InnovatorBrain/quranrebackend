# Generated by Django 5.0.6 on 2024-05-27 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_account', '0002_customuser_is_student_customuser_is_teacher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='enrolled_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='grade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='parent_contact',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='subject',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
