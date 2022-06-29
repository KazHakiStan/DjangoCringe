from django.contrib import admin
from .models import Chat


@admin.register(Chat)
class FriendshipAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver', ]
    list_display = ['sender', 'receiver', ]
    search_fields = ['sender', 'receiver', ]

    class Meta:
        model = Chat
