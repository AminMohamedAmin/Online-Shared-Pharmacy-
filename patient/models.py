from django.db import models

# Create your models here.

class Question(models.Model):
    user = models.CharField(max_length=150)
    quest = models.CharField(max_length=500)
    reply = models.CharField(max_length=500)
    admin = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

class Messages(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)