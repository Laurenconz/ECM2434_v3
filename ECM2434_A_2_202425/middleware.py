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
        # Fix incorrect API base (e.g., /localhost:8000/api/...)
        if request.path.startswith('/localhost:8000/api/'):
            corrected_path = request.path.replace('/localhost:8000', '')
            request.META['PATH_INFO'] = corrected_path
            print(f"[Middleware] Corrected path: {corrected_path}")

        # Continue processing
        response = self.get_response(request)
        return response
