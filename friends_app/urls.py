from django.contrib.auth.decorators import login_required
from django.urls import path, include

from friends_app.views import friendship


urlpatterns = [
    path('connect/<str:action>/<int:pk>', login_required(friendship), name='friendship'),
]