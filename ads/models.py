from django.db.models import TextChoices
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lng = models.DecimalField(max_digits=10, decimal_places=8)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class UserRoles(TextChoices):
    MEMBER = "member", "Пользователь"
    ADMIN = "admin", "Админ"
    MODERATOR = "moderator", "Модер"


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.MEMBER)
    age = models.PositiveIntegerField()
    location = models.ManyToManyField("Location")

    class Meta:
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey("ads.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey("ads.Category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ad_image", blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-price"]
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name

