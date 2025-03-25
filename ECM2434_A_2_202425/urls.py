from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("<html><body><h1>Django is working!</h1><p>This test view confirms the basic functionality.</p></body></html>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bingo.urls')),
    path('test/', test_view),
    path('', TemplateView.as_view(template_name='index.html')),
]

# Add this section to serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)