from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='users/%Y', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'