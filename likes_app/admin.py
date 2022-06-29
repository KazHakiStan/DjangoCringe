from django.contrib import admin
from likes_app.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id',)
    ordering = ('-id',)

