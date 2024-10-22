from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils import translation

class LanguageRouterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/en') or request.path.startswith('/fr'):
            # Language already in URL, no need to redirect
            return self.get_response(request)

        # Get language from the session or browser
        language = request.session.get('django_language', request.LANGUAGE_CODE)
        if not language:
            language = translation.get_language_from_request(request)

        # Redirect to the appropriate language URL
        if language == 'fr':
            return HttpResponseRedirect('/fr' + request.path)
        else:
            return HttpResponseRedirect('/en' + request.path)

        return self.get_response(request)