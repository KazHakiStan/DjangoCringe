from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User

from likes_app.models import Like
from publication_app.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    text = models.CharField(max_length=256, blank=False, verbose_name='Комментарий')
    created_time = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return f'{self.text}'

    @property
    def total_likes(self):
        return self.likes.count()
