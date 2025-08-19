# posts/views_html.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, PostForm 
from .models import Post, Comment
from .forms import CommentForm, PostForm
# -----------------------------
# Profile View (User Profile + Post Form)
# -----------------------------
# -----------------------------
# Static Pages
# -----------------------------
def home(request):
    return render(request, "posts/home.html")

def about(request):
    return render(request, "posts/about.html")

def contact(request):
    return render(request, "posts/contact.html")


# -----------------------------
# Post Views (Require Login)
# -----------------------------
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
    template_name = "posts/post_form.html"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_list")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "posts/post_form.html"
    fields = ['title', 'content']

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_list")


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_list")


# -----------------------------
# Comment View (Requires Login)
# -----------------------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_form.html"

    def form_valid(self, form):
        post_id = self.kwargs.get("post_id")
        form.instance.post = get_object_or_404(Post, id=post_id)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})
