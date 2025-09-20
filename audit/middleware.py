import logging
from datetime import datetime

access_logger = logging.getLogger("audit.access")

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else None
        ip = request.META.get("REMOTE_ADDR")
        method = request.method
        path = request.get_full_path()

        access_logger.info(f"{datetime.now()} | {ip} | {user} | {method} {path}")

        response = self.get_response(request)
        return response
