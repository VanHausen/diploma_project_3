from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователь"