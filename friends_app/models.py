from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Friendship(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    is_sub = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)
    wait_answer = models.BooleanField(default=True)

    def __str__(self):
        return f'sender:{self.sender}->receiver:{self.receiver}'