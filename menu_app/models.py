from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Menu(models.Model):
    menu_label = models.CharField(max_length=256, null=False, blank=False, unique=True)

    def __str__(self):
        return f'{self.id}: {self.menu_label}'


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, null=False, blank=False, on_delete=models.PROTECT, related_name='links')
    title = models.CharField(max_length=32, null=False, blank=False)
    url = models.CharField(max_length=256, null=False, blank=False)
    icon = models.ImageField(null=True, blank=True)
    priority = models.SmallIntegerField(validators=[MinValueValidator(-100), MaxValueValidator(100)], default=0)

    def __str__(self):
        return f'{self.id}: {self.title}'

    class Meta:
        indexes = [
            models.Index(fields=('menu',)),
            models.Index(fields=('menu', 'url'))
        ]
        unique_together = [('menu', 'title')]