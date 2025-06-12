from django.http import HttpResponse

class CustomCORSHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('here')
        # Handle preflight OPTIONS request early
        if request.method == "OPTIONS":
            response = HttpResponse()
            self.add_cors_headers(response, request)
            response.status_code = 200
            return response

        response = self.get_response(request)
        self.add_cors_headers(response, request)
        return response

    def add_cors_headers(self, response, request):
        origin = request.headers.get("Origin")
        response["Access-Control-Allow-Origin"] = origin if origin else "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, PATCH, DELETE"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        response["Access-Control-Allow-Credentials"] = "true"