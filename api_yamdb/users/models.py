from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для работы с пользователями"""
    CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=254,
        unique=True,
        blank=False
    )
    bio = models.TextField(blank=True,)
    role = models.CharField(max_length=15, choices=CHOICES, default='user')
    confirmation_code = models.CharField(
        max_length=255, blank=True, null=True
    )
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email',),
                name='unique_fields'
            ),
        ]

    def __str__(self) -> str:
        return self.username
