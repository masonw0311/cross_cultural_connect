from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    country_of_origin = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username}, {self.password}"