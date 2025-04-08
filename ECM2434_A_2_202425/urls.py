from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from PIL import Image
import io
import requests

@csrf_exempt
def placeholder_proxy(request, size):
    """Proxy requests to placeholder service"""
    try:
        response = requests.get(f"https://via.placeholder.com/{size}")
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    except:
        # Return a simple colored square if the service is unavailable
        # Parse size
        try:
            width, height = size.split('x')
        except:
            width = height = size
            
        # Create a simple colored square
        img = Image.new('RGB', (int(width), int(height)), color=(200, 200, 200))
        response = HttpResponse(content_type='image/png')
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        response.write(img_io.read())
        return response
    
@csrf_exempt
def api_proxy(request, path):
    """Redirect localhost API calls to the actual API"""
    # Forward the request to the actual API endpoint
    new_path = f"/api/{path}"
    return redirect(new_path)
    
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Add a specific route for your template HTML files
    path('developer-front.html', TemplateView.as_view(template_name='developer-front.html')),
    path('gamekeeper.html', TemplateView.as_view(template_name='gamekeeper.html')),
    
    # Add a direct route to the static gamekeeper page
    path('gamekeeper-static/', TemplateView.as_view(template_name='gamekeeper.html')),
    
    # API routes
    path('api/', include('bingo.urls')),
    
    # Proxy routes
    path('via.placeholder.com/<str:size>', placeholder_proxy),
    re_path(r'^localhost:8000/api/(?P<path>.*)$', api_proxy),
    
    # React app routes - catches everything else
    path('gamekeeper/', TemplateView.as_view(template_name='index.html')),
    path('gk/', TemplateView.as_view(template_name='index.html')),
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^(?!api/|admin/|developer-front\.html|gamekeeper\.html|gamekeeper-static/).*$', 
            TemplateView.as_view(template_name='index.html')),
]

# Add this for development (will be ignored in production with DEBUG=False)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)