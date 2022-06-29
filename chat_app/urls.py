from django.contrib.auth.decorators import login_required
from django.urls import path, include

from chat_app.views import ChatView

urlpatterns = [
    path('message/<int:pk>', login_required(ChatView.as_view()), name='chat'),
]