from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Email(models.Model):
    name = models.CharField(max_length=20, default="New Email")
    subject_line = models.CharField(max_length=60)
    email_content = models.TextField()

    def __str__(self):
        return f"{self.name}: {self.subject_line}"



class EmailRecords(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=300, default="New Subject")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
