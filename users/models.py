from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.constants import (
    AVATAR_UPLOAD_PATH,
    DEFAULT_AVATAR,
    MAX_ABOUT_LEN,
    MAX_NAME_LEN,
    MAX_PHONE_LEN,
    MAX_SURNAME_LEN,
)
from users.managers import UserManager
from users.utils import create_avatar


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        unique=True, verbose_name="Электронная почта"
    )
    name = models.CharField(max_length=MAX_NAME_LEN, verbose_name="Имя")
    surname = models.CharField(
        max_length=MAX_SURNAME_LEN, verbose_name="Фамилия")
    avatar = models.ImageField(
        upload_to=AVATAR_UPLOAD_PATH, default=DEFAULT_AVATAR, verbose_name="Аватар"
    )
    phone = models.CharField(max_length=MAX_PHONE_LEN,
                             verbose_name="Номер телефона")
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    about = models.TextField(
        max_length=MAX_ABOUT_LEN, blank=True, verbose_name="О себе"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")

    favorites = models.ManyToManyField(
        "projects.Project",
        blank=True,
        related_name="interested_users",
        verbose_name="Избранные проекты",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-email"]  

    def __str__(self):
        return f"{self.name} {self.surname}"

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.avatar or self.avatar.name == DEFAULT_AVATAR:
            self.avatar = create_avatar(self.name, self.email)
        super().save(*args, **kwargs)