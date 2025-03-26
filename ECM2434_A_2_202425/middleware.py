import re
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import urlparse
import requests
from io import BytesIO
from PIL import Image

class RequestFixerMiddleware:
    """
    Middleware to fix request URLs that might be incorrectly configured
    in the frontend after deployment
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Convert localhost API requests to relative paths
        if request.path.startswith('/localhost:8000/api/'):
            # Strip off the localhost part
            corrected_path = request.path.replace('/localhost:8000/api/', '/api/')
            request.path = corrected_path
            request.path_info = corrected_path
        
        # Handle any other path fixups here as needed
        
        # Continue processing the request
        response = self.get_response(request)
        return response