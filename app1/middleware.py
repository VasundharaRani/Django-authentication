import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)

class ExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception occurred: {exception}", exc_info=True)

        return render(request, 'error.html', {'message': str(exception)}, status=500)
