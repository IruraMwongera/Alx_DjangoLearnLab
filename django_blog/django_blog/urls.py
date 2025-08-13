from django.contrib import admin
from django.urls import path, include
from blog.views import home  # use your home view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL goes to home() which decides where to send the user
    path('', home, name='home'),

    # Blog URLs
    path('', include('blog.urls')),
]
