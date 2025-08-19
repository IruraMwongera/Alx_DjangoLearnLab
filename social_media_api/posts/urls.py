from django.urls import path
from . import views_html  # or from . import views (choose one)

urlpatterns = [
    path("", views_html.PostListView.as_view(), name="post_list"),
    path("<int:pk>/", views_html.PostDetailView.as_view(), name="post_detail"),
    path("new/", views_html.PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/edit/", views_html.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", views_html.PostDeleteView.as_view(), name="post_delete"),
    path("<int:post_id>/comment/", views_html.CommentCreateView.as_view(), name="add_comment"),
]