from django.conf import settings
from django.utils import translation


class URLPrefixLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info or "/"
        active = settings.LANGUAGE_CODE

        for code, _name in settings.LANGUAGES:
            if path == f"/{code}" or path.startswith(f"/{code}/"):
                active = code
                break

        translation.activate(active)
        request.LANGUAGE_CODE = active
        return self.get_response(request)