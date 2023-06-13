from django.db import models


# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=50, default="New Plan")
    color = models.CharField(max_length=7, null=True)
    price = models.IntegerField(null=True)
    provider = models.CharField(max_length=20, null=True)
    slug = models.SlugField(max_length=10, null=True)

    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f"{self.name}: {self.provider} - {self.price}"
