from django.db import models


class Vehicle(models.Model):
    model = models.CharField(max_length=30, blank=False, null=False)
    horsepower = models.CharField(max_length=30, blank=False, null=False)
    torque = models.CharField(max_length=25, blank=False, null=False)
    price = models.CharField(max_length=20, blank=False, null=False)


def __str__(self):
    return self.name