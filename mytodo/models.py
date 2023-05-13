from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

class Tasking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)
    reminder_time = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.due_date < timezone.now()

    def send_reminder(self):
        if self.reminder_time > 0:
            reminder_date = self.due_date - timezone.timedelta(minutes=self.reminder_time)
            current_date = timezone.now()
            if current_date >= reminder_date:
                recipient_email = self.user.email
                subject = f"Reminder: {self.task}"
                message = f"Hello {self.user.username},\n\nThis is a reminder for your task: {self.task}.\n\nPlease complete it before the due date: {self.due_date}.\n\nBest regards,\nThe Todo App Team"
                send_mail(subject, message, "your-email@example.com", [recipient_email], fail_silently=False)
        # Implement reminder email sending here


