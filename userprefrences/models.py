from email.policy import default
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from sklearn.feature_extraction import image
# Create your models here.


class UserPrefrence(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user)+'\'s'+' preferences'


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name='Profile')
    image = models.ImageField(upload_to='pics', default='media/default.png')
    name=models.CharField(default='Name Surname',max_length=200,null=True)

    def __str__(self):
        return str(self.user)+'\'s'+' profile'
