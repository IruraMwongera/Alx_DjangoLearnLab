from . import views
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
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.BlogLoginView.as_view(), name='login'),
    path('logout/', views.BlogLogoutView.as_view(), name='logout'),
]



