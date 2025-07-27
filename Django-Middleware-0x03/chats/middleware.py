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