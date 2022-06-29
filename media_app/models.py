from django.db import models
from django.contrib.auth.models import User


class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    file = models.ImageField(blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)