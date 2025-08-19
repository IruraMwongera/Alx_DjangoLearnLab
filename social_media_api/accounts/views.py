from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView
from .forms import ProfileUpdateForm
from posts.forms import PostForm
# -----------------------------
# Home View - Redirect Logic
# -----------------------------
def home(request):
    if request.user:
        return redirect('post-list')

# -----------------------------
# Login & Logout Views
# -----------------------------
class accountsLoginView(LoginView):
    template_name = 'accounts/login.html'

class accountsLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'
    next_page = reverse_lazy('login')

# -----------------------------
# User Registration
# -----------------------------
def register(request):
    if request.user.is_authenticated:
        return redirect('post-list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account was created. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# -----------------------------
# Profile Management
# -----------------------------
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)  # fixed
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def profile_view(request):
    profile_form = ProfileUpdateForm(instance=request.user)
    post_form = PostForm()

    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect("profile")

        elif "create_post" in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect("profile")

    return render(request, "accounts/profile.html", {
        "form": profile_form,
        "post_form": post_form
    })



