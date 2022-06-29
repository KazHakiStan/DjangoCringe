from django.db.models.signals import post_save
from django.dispatch import receiver
from profile_app.models import Profile, User


@receiver(post_save, sender=User)
def post_created_profile(instance, created, **kwargs):
    """Создания записи в модели Profile"""

    # Получаем объект user
    user = User.objects.get(pk=instance.id)

    if created:
        user_add = Profile(user=user)
        user_add.save()