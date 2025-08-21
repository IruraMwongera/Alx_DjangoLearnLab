# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'

urlpatterns = [
    # ------------------
    # Specific, static URLs should always come first
    # ------------------
    path('login/', views.accountsLoginView.as_view(), name='login'),
    path('logout/', views.accountsLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    
    # -----------------------------------------------------------
    # Corrected Follow/Unfollow URLs (point to functions, not classes)
    # -----------------------------------------------------------
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),

    # ---------------------------------------------------------------
    # The generic profile URL must come LAST
    # It catches any string that didn't match the URLs above it
    # ---------------------------------------------------------------
    path('<str:username>/', views.user_profile_view, name='user_profile'),
]