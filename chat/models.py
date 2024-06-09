from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    key = models.CharField(max_length=255, unique=True)
    url_path = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    encrypted_content = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)
