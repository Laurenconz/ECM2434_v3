from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Remove or comment out this function
# def home(request):
#     return HttpResponse("Hello, Django is running!")

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel
    path('api/', include('bingo.urls')),  # Include API routes with 'api/' prefix
    
    # Use the staticfiles index.html as your main template
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]


# Debug Toolbar (Only if settings.DEBUG is True)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)