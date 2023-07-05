from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db.models import TextChoices, UniqueConstraint
from django.db import models

from HW_27.settings import FORBIDDEN_DOMAIN
from ads.validators import check_age


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
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.ManyToManyField('ads.Location')
    birth_date = models.DateField(null=True, blank=True, validators=[check_age])
    email = models.EmailField(
        validators=[RegexValidator(
            regex=FORBIDDEN_DOMAIN,
            message='Домен запрещен',
            inverse_match=True
        )],
        unique=True
    )

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
    slug = models.SlugField(max_length=10, validators=[MinLengthValidator(5)], unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=150, validators=[MinLengthValidator(10)])
    author = models.ForeignKey("ads.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey("ads.Category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ad_image", blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-price"]
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name

