from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from .views import MainPage, UserLogin, Register, Profile, user_logout, UserRedaction, ProfileUserView, \
    UserSearchListView

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    path('red/', login_required(UserRedaction.as_view()), name='red'),
    path('profile/', login_required(Profile.as_view()), name='profile'),
    path('profile/<int:pk>', login_required(ProfileUserView.as_view()), name='profile_user'),
    path('search/', UserSearchListView.as_view(), name='user_search'),
]