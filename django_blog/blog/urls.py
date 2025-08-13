from django.urls import path
from .views import (
    BlogLoginView,
    BlogLogoutView,
    register,
    profile,
    post_list,  # Make sure you have this view in views.py
)

urlpatterns = [
    path('login/', BlogLoginView.as_view(), name='login'),
    path('logout/', BlogLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('posts/', post_list, name='posts'),  # List of all blog posts
]
