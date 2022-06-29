from django import forms

from chat_app.models import Chat


class ChatForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ['text', 'receiver', 'sender']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
            "sender": forms.HiddenInput(),
            "receiver": forms.HiddenInput(),
        }