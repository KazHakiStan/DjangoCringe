from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from publication_app.views import Posts, AddPost, ReadPostView, EditImagePost, post_delete, Tags, GetTag

urlpatterns = [
    path('posts/', Posts.as_view(), name='posts'),
    path('post/<int:pk>', login_required(ReadPostView.as_view()), name='post'),
    path('add_post/', login_required(AddPost.as_view()), name='add_post'),
    path('post_red/<int:pk>', login_required(EditImagePost.as_view()), name='post_red'),
    path('post_del/<int:pk>', login_required(post_delete), name='post_del'),
    path('tags/', Tags.as_view(), name='tags'),
    path('tag/<str:tag>/', GetTag.as_view(), name='tag'),
]