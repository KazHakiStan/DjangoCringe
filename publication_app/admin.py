from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from publication_app.models import Post, ImagePost


class PostWithImage(admin.StackedInline):
    model = ImagePost
    max_num = 4
    extra = 0
    list_display = ('id', 'image_tag', 'post_id')
    ordering = ('-post_id',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(
                f'<a href="{obj.image.url}">'
                f'<img src="{obj.image.url}" width ="150" height="150" />'
                f'</a>'
            )

    image_tag.short_description = 'Фото к посту'
    image_tag.allow_tags = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (PostWithImage,)

    list_display = ('id', 'created_time', 'title', 'is_public',)
    ordering = ('-created_time', '-id')
    readonly_fields = ('created_time',)
    # изменять не заходя в пост
    list_editable = ('is_public', )
    # фильтровать по чем
    list_filter = ('is_public',)



