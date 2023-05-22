from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=150)
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=150)
