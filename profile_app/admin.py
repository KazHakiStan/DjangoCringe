from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth.models import User
from profile_app.models import Profile
from django.utils.html import mark_safe


admin.site.unregister(User)


class ProfileInline(admin.StackedInline):

    model = Profile
    list_display = ('user', 'date_of_birth', 'photo_tag')
    ordering = ('-user',)
    readonly_fields = ('photo_tag',)

    def photo_tag(self, obj):
        if obj.photo:
            return mark_safe(
                f'<a href="{obj.photo.url}">'
                f'<img src="{obj.photo.url}" width ="150" height="150"/><a href="{obj.photo.url}"/>'
                f'</a>'
            )

    photo_tag.short_description = 'Аватар'
    photo_tag.allow_tags = True


@admin.register(User)
class UserAdmin(UserAdminBase):
    inlines = (
        ProfileInline,
    )