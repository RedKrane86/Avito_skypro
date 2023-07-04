from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, UniqueConstraint
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


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.MEMBER)
    age = models.PositiveIntegerField()
    location = models.ManyToManyField("Location")

    def save(self, *args, **kwargs):
        self.set_password(raw_password=self.password)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Selection(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('ads.User', on_delete=models.CASCADE)
    items = models.ManyToManyField('ads.Ad')

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"
        constraints = [UniqueConstraint(fields=['name', 'owner'], name='owner_constraint')]

    def __str__(self):
        return self.name


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

