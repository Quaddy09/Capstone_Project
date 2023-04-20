from django.db import models


class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.username


class Room(models.Model):
    room_name = models.CharField(max_length=60)
    players = models.JSONField(default=list)

    def __str__(self) -> str:
        return self.room_name
