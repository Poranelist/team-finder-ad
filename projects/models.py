from django.contrib.auth import get_user_model
from django.db import models

from core.constants import (MAX_PROJECT_NAME_LEN, PROJECT_STATUS_CHOICES,
                            PROJECT_STATUS_CLOSED, PROJECT_STATUS_OPEN)

User = get_user_model()


class Project(models.Model):

    name = models.CharField(
        max_length=MAX_PROJECT_NAME_LEN, verbose_name="Название")

    description = models.TextField(blank=True, verbose_name="Описание")

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")

    status = models.CharField(
        max_length=max(len(status[0]) for status in PROJECT_STATUS_CHOICES),
        choices=PROJECT_STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN,
        verbose_name="Статус",
    )

    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="participated_projects",
        verbose_name="Участники",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name
