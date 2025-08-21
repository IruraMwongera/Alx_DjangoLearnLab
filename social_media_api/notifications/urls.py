# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Reference the new function-based view directly
    path('', views.notification_list, name='notification-list'),
    
    # Reference the new function-based view directly
    path('<int:pk>/read/', views.mark_as_read, name='notification-mark-read'),
]