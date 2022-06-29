from django import forms
from django.contrib.auth.models import User
from profile_app.models import Profile


class UserEditForm(forms.ModelForm):
    """Класс форма редактирование User"""
    first_name = forms.CharField(
        label='Имя'
    )
    last_name = forms.CharField(
        label='Фамилия'
    )
    email = forms.EmailField(
        label='email'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    """Класс форма редактирование Profile"""

    class Meta:
        model = Profile
        fields = ['photo',]