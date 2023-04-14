from django.db import models


class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.username


class Lobby(models.Model):
    room_name = models.CharField(max_length=50)
    players = models.ManyToManyField(User)

    def __str__(self) -> str:
        return self.lobby_name

