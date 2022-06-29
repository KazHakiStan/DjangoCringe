from django import forms

from comments_app.models import Comment


class AddCommentsForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["post", "user", "text"]
        widgets = {
            "post": forms.HiddenInput(),
            "user": forms.HiddenInput(),
        }