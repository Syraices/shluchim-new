from django.db import models

# Create your models here.
class Email(models.Model):
    name = models.CharField(max_length=20, default="New Email")
    subject_line = models.CharField(max_length=60)
    email_content = models.TextField()

    def __str__(self):
        return f"{self.name}: {self.subject_line}"