from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Location(models.Model):
    name = models.TextField(max_length=50, null=True, blank=True, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    class Meta():
        ordering = ['-created']


class Customer(models.Model):
    name = models.TextField(max_length=50)
    shop_name = models.TextField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Session(models.Model):
    name = models.TextField(max_length=50, null=True, blank=True, unique=True)
    customer = models.ManyToManyField(Customer, related_name='customers')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | {self.created}'
    class Meta():
        ordering = ['-created']
