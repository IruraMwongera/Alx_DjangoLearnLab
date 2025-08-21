# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# This is the crucial line for namespacing
app_name = 'posts'

# ----------------------------------------------------
# 1. Router for DRF API ViewSets
# The router will handle /api/posts/ and /api/comments/
# ----------------------------------------------------
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='api-post')
router.register(r'comments', views.CommentViewSet, basename='api-comment')

# ----------------------------------------------------
# 2. Main URL Patterns for both HTML and API views
# ----------------------------------------------------
urlpatterns = [
    # HTML Views (The order matters here)
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('feed/', views.feed_view, name='feed'),
    
    # New HTML endpoints for liking and unliking
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
    
    # API Endpoints (Now they have a distinct /api/ prefix)
    path('api/', include(router.urls)),
]