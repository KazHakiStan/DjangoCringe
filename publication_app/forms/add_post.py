from django import forms
from django.core.exceptions import ValidationError
import re

from publication_app.models import Post
from tags_app.models import Tag


class AddPostForm(forms.ModelForm):
    """Класс формы добавление поста"""
    title = forms.CharField(label='Введите название поста*')
    text = forms.CharField(
        label='Введите тест к посту*',
        widget=forms.Textarea()
    )
    is_public = forms.BooleanField(
        label='Публичная запись ?',
        initial=True,
        required=False
    )

    tag = forms.ModelMultipleChoiceField(
        label='Тэги',
        required=False,
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'is_public', 'tag']


class ImagePostForm(AddPostForm):

    image = forms.ImageField(
        label='Выберите фотографии',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta(AddPostForm.Meta):
        fields = AddPostForm.Meta.fields + ['image', ]
