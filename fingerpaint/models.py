from django.db import models


class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=40)

    def __str__(self):
        return self.username
