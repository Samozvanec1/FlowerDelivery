from django.db import models
from datetime import datetime
from asgiref.sync import sync_to_async


class Flower(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    tg_id = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order of {self.flower.title} by {self.user.name}"