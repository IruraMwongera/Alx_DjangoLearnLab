from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import UserRegisterForm, ProfileUpdateForm
from posts.models import Post
from .models import CustomUser

# -----------------------------
# Login & Logout Views
# -----------------------------
class accountsLoginView(LoginView):
    template_name = 'accounts/login.html'

class accountsLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'
    next_page = reverse_lazy('accounts:login')  # FIXED: Added 'accounts:' namespace

# -----------------------------
# User Registration
# -----------------------------
def register(request):
    if request.user.is_authenticated:
        return redirect('posts:post_list')  # FIXED: Added 'posts:' namespace

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account was created. You can now log in.')
            return redirect('accounts:login')  # FIXED: Added 'accounts:' namespace
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# -----------------------------
# Profile Display Views
# -----------------------------
@login_required
def profile_view(request):
    """
    Displays the profile of the currently logged-in user.
    """
    user_posts = request.user.posts.all().order_by("-created_at")
    
    return render(request, "accounts/profile.html", {
        "user_profile": request.user,
        "user_posts": user_posts,
    })

def user_profile_view(request, username):
    """
    Displays the profile of a user based on their username.
    """
    user_profile = get_object_or_404(CustomUser, username=username)
    user_posts = user_profile.posts.all().order_by("-created_at")
    
    return render(request, "accounts/profile.html", {
        "user_profile": user_profile,
        "user_posts": user_posts,
    })


# -----------------------------
# Profile Update View
# -----------------------------
@login_required
def profile_update_view(request):
    """
    Handles the form for updating the user's profile using a single form.
    """
    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("accounts:profile") # FIXED: Added 'accounts:' namespace
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
    
    return render(request, "accounts/profile_update.html", {
        "form": profile_form
    })