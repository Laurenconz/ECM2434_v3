import re
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import urlparse
import requests
from io import BytesIO
from PIL import Image

class RequestFixerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Compile the regex patterns once for efficiency
        self.localhost_pattern = re.compile(r'localhost:8000/api/')
        self.placeholder_pattern = re.compile(r'via\.placeholder\.com/(\d+)')

    def __call__(self, request):
        # Check if this is a request to localhost API
        path = request.path_info
        
        # Handle localhost:8000/api requests
        if 'localhost:8000/api/' in path:
            new_path = path.replace('localhost:8000/api/', '/api/')
            return HttpResponseRedirect(new_path)
            
        # Handle placeholder image requests  
        placeholder_match = self.placeholder_pattern.search(path)
        if placeholder_match:
            size = placeholder_match.group(1)
            # Create a simple placeholder image
            width = height = int(size)
            img = Image.new('RGB', (width, height), color=(200, 200, 200))
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)
            
            return HttpResponse(
                content=img_io.getvalue(),
                content_type='image/png'
            )
            
        # Process the regular response for all other requests
        response = self.get_response(request)
        return response
