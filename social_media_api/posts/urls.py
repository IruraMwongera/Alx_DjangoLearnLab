# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'posts'

# ----------------------------------------------------
# Router for DRF API ViewSets
# ----------------------------------------------------
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='api-post')
router.register(r'comments', views.CommentViewSet, basename='api-comment')

# ----------------------------------------------------
# Main URL Patterns
# ----------------------------------------------------
urlpatterns = [
    # HTML Views
    path("", views.HomePostListView.as_view(), name="home"),  # Homepage = latest 10 posts
    path("posts/", views.PostListView.as_view(), name="post_list"),  # full list of all posts
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/<int:post_id>/comment/", views.CommentCreateView.as_view(), name="comment_create"),
    path("feed/", views.feed_view, name="feed"),

    # Like / Dislike (Toggles only)
    path("post/<int:pk>/like/", views.like_post, name="like_post"),
    path("post/<int:pk>/dislike/", views.dislike_post, name="dislike_post"),

    # API Endpoints
    path("api/", include(router.urls)),

    # API Like/Dislike toggle
    path("api/posts/<int:pk>/like/", views.PostLikeToggleAPIView.as_view(), name="api_post_like"),
    path("api/posts/<int:pk>/dislike/", views.PostDislikeToggleAPIView.as_view(), name="api_post_dislike"),
]
