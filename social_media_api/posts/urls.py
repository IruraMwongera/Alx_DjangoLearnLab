from django.urls import path
from . import views

# This is the crucial line for namespacing
app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    # Delete or comment out this line:
    # path('post/search/', views.PostSearchView.as_view(), name='post_search'),
]