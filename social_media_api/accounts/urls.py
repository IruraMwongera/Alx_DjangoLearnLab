from django.urls import path
from . import views
from .views import (
    accountsLoginView,
    accountsLogoutView,
    register,
    profile,
    profile_view 
    )

urlpatterns = [
    # Auth & Profile
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', accountsLoginView.as_view(), name='login'),
    path('logout/', accountsLogoutView.as_view(), name='logout'),
    path("profile/update/", views.profile_view, name="profile"),
]