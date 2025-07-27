import logging

# Configure basic logging (optional, for demonstration)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Initializes the middleware.
        
        Args:
            get_response: A callable representing the next middleware or the view.
        """
        self.get_response = get_response
        # One-time configuration or setup can be done here.
        logging.info("RequestLoggingMiddleware initialized.")

    def __call__(self, request):
        """
        Processes the incoming request and logs details.
        
        Args:
            request: The incoming request object.
        
        Returns:
            The response object after processing.
        """
        # Log request details before processing
        logging.info(f"Incoming Request: Method={request.method}, Path={request.path}")

        # Call the next middleware or the view to get the response
        response = self.get_response(request)

        # Log response details after processing (optional)
        logging.info(f"Outgoing Response: Status={response.status_code}")

        return response
      
      
      
      
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Optional: define allowed time window
        self.allowed_start = time(18, 0)  # 6 PM
        self.allowed_end = time(21, 0)    # 9 PM

    def __call__(self, request):
        current_time = datetime.now().time()

        # Check if current time is outside allowed time
        if not (self.allowed_start <= current_time <= self.allowed_end):
            return HttpResponseForbidden("Access to this page is restricted outside 6 PM to 9 PM.")

        return self.get_response(request)


import time
from django.http import HttpResponseTooManyRequests
from collections import defaultdict
from threading import Lock

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track timestamps of requests per IP
        self.ip_message_log = defaultdict(list)
        self.lock = Lock()
        self.message_limit = 5           # Max messages
        self.time_window = 60            # Time window in seconds (1 minute)

    def __call__(self, request):
        # Only apply rate limit to POST requests (e.g., chat messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            current_time = time.time()

            with self.lock:
                timestamps = self.ip_message_log[ip]
                # Remove timestamps older than 1 minute
                self.ip_message_log[ip] = [
                    t for t in timestamps if current_time - t < self.time_window
                ]

                if len(self.ip_message_log[ip]) >= self.message_limit:
                    return HttpResponseTooManyRequests(
                        "Rate limit exceeded: Max 5 messages per minute allowed."
                    )

                # Log current request timestamp
                self.ip_message_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Safely extracts the client's IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip



from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only proceed if user is authenticated
        user = getattr(request, 'user', None)

        if user is None or not user.is_authenticated:
            return HttpResponseForbidden("Access Denied: Authentication required.")

        # Check if user has required role
        if user.role not in ['admin', 'moderator']:
            return HttpResponseForbidden("Access Denied: Insufficient role permissions.")

        return self.get_response(request)
