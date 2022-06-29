from django.contrib import admin
from .models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver', 'is_accepted']
    list_display = ['sender', 'receiver', 'is_accepted']
    search_fields = ['sender', 'receiver', 'is_accepted']
    # readonly_fields = ['sender']

    class Meta:
        model = Friendship
