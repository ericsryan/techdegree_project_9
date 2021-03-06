from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_date = models.DateField(
            default=timezone.now)
    expiration_date = models.DateField()


    def __str__(self):
        return self.season

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateField(
            default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
