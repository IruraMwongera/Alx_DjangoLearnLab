from django.urls import path
from .views import (
    BlogLoginView,
    BlogLogoutView,
    register,
    profile,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    # Auth & Profile
    path('login/', BlogLoginView.as_view(), name='login'),
    path('logout/', BlogLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    # Blog Post CRUD
    path('posts/', PostListView.as_view(), name='post-list'),                   # List all posts
    path('posts/new/', PostCreateView.as_view(), name='post-create'),           # Create new post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),      # View post details
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'), # Edit post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # Delete post
]
