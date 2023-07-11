from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    modified_on = models.DateTimeField(auto_now=True)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, null=True)
    address = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='images/')


class Group(models.Model):
    name = models.CharField(unique=True, max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
