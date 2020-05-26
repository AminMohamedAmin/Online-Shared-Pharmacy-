from django.db import models

# Create your models here.

class Actions(models.Model):
    type = models.CharField(max_length=200, default='')
    action = models.CharField(max_length=200, default='')
    created = models.DateTimeField(auto_now_add=True)
    day = models.DateField(auto_now_add=True)