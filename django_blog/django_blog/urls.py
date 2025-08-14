from django.contrib import admin
from django.urls import path, include
from blog.views import home  # use your home view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL goes to home() which decides where to send the user
    path('', home, name='home'),

    # Blog URLs
    path('', include('blog.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
