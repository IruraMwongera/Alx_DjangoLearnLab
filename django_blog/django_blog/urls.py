from django.contrib import admin
from django.urls import path, include
from blog.views import register  # import your register view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL will show the registration page
    path('', register, name='home'),

    # Blog URLs
    path('', include('blog.urls')),
]
