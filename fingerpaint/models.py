from django.db import models


class Lobby(models.Model):
    lobby_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.lobby_name
# lobby = models.ForeignKey(Lobby.lobby_name, on_delete=models.CASCADE)


class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.username
