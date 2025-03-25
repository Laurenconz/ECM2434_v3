from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bingo.urls')),
    
    # Serve the React app for all non-API, non-admin routes
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^(?!api/|admin/).*$', TemplateView.as_view(template_name='index.html')),
]

# Add this for development (will be ignored in production with DEBUG=False)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)