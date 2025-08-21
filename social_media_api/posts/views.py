from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .forms import PostForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Post


# DRF API Views (No changes needed here for now)
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit/delete their own objects.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# -----------------------------------
# HTML Views for templates
# -----------------------------------
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ['-created_at']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # FIX: Added 'posts:' namespace
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        # FIX: Added 'posts:' namespace
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        # FIX: Added 'accounts:' namespace
        return reverse_lazy('accounts:profile')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_form.html"

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        form.instance.post = get_object_or_404(Post, pk=post_id)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # FIX: Added 'posts:' namespace
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return context
@login_required
def feed_view(request):
    """
    Generates a feed of posts from users the current user is following.
    """
    # Get the list of users the current user is following
    # Change the variable name to 'following_users' to match the check
    following_users = request.user.following.all()
    
    # Get posts from all followed users, ordered by creation date
    feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    context = {
        'feed_posts': feed_posts
    }
    return render(request, 'posts/feed.html', context)