# posts/views.py

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from .models import Post, Comment, Like, Dislike
from .serializers import PostSerializer, CommentSerializer
from .forms import PostForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.http import require_POST

# -----------------------
# DRF API Permissions
# -----------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# -----------------------
# DRF API ViewSets
# -----------------------
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

class HomePostListView(ListView):
    model = Post
    template_name = "posts/home.html"   # create this template
    context_object_name = "posts"
    paginate_by = None  # optional, if you don’t want pagination

    def get_queryset(self):
        return Post.objects.order_by("-created_at")[:10]  # latest 10


# -----------------------
# HTML Views
# -----------------------
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ['-created_at']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_user_liked'] = self.object.likes.filter(user=self.request.user).exists()
            context['has_user_disliked'] = self.object.dislikes.filter(user=self.request.user).exists()
        else:
            context['has_user_liked'] = False
            context['has_user_disliked'] = False
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
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
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return context


@login_required
def feed_view(request):
    following_users = request.user.following.all()
    feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    return render(request, 'posts/feed.html', {'feed_posts': feed_posts})


# -----------------------
# DRF API Like/Dislike (Mutually Exclusive)
# -----------------------
class PostLikeToggleAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Remove dislike if user had disliked
        Dislike.objects.filter(user=request.user, post=post).delete()

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
        else:
            if request.user != post.author:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked',
                    target_content_type=ContentType.objects.get_for_model(Post),
                    target_object_id=post.id
                )
            return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)


class PostDislikeToggleAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Remove like if user had liked
        Like.objects.filter(user=request.user, post=post).delete()

        dislike, created = Dislike.objects.get_or_create(user=request.user, post=post)

        if not created:
            dislike.delete()
            return Response({"message": "Post undisliked."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Post disliked."}, status=status.HTTP_201_CREATED)


# -----------------------
# HTML Views Like/Dislike (Mutually Exclusive)
# -----------------------
@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Remove dislike if it exists
    Dislike.objects.filter(user=request.user, post=post).delete()

    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if created:
        messages.success(request, "Post liked!")
        if request.user != post.author:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id
            )
    else:
        like.delete()
        messages.success(request, "Like removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('posts:post_list')))


@login_required
@require_POST
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Remove like if it exists
    Like.objects.filter(user=request.user, post=post).delete()

    dislike, created = Dislike.objects.get_or_create(user=request.user, post=post)

    if created:
        messages.success(request, "Post disliked!")
    else:
        dislike.delete()
        messages.success(request, "Dislike removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('posts:post_list')))