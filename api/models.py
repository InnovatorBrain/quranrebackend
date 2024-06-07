from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from auth_account.models import CustomUser, StudentProfile, TeacherProfile

class Todo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:30]

class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="chat_messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    recipient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="received_messages")

    message = models.CharField(max_length=10000000000)

    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.sender} - {self.recipient}"

    @property
    def sender_profile(self):
        return self.sender.student_profile if hasattr(self.sender, 'student_profile') else self.sender.teacher_profile

    @property
    def recipient_profile(self):
        return self.recipient.student_profile if hasattr(self.recipient, 'student_profile') else self.recipient.teacher_profile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        if instance.is_teacher:
            TeacherProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_student:
        instance.student_profile.save()
    if instance.is_teacher:
        instance.teacher_profile.save()
