from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Изменение встроенного профиля AbstractUser с возможностью добавления картинки"""
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
