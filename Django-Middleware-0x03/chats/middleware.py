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
