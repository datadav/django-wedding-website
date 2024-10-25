from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils import translation

import os


def print_directory_contents(path):
    if "/app/static" not in path:
        return
    for root, dirs, files in os.walk(path):
        for file_name in files:
            print(f"  File: {root}/{file_name}")


class LanguageRouterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude static and media files from redirection
        current_directory = os.getcwd()
        # print_directory_contents(current_directory)
        print_directory_contents("/app/static")
        print("request.path", request.path)
        print("is exists", os.path.exists("/app/static/bigday/js/footer.js"))
        print(os.listdir("/app/static"))
        if request.path.startswith("/app/static"):
            return self.get_response(request)

        if request.path.startswith('/en') or request.path.startswith('/fr'):
            # Language already in URL, no need to redirect
            return self.get_response(request)
        

        # Get language from the session or browser
        language = request.session.get('django_language', request.LANGUAGE_CODE)
        print("language", language)
        if not language:
            language = translation.get_language_from_request(request)

        # Redirect to the appropriate language URL
        if language == 'fr':
            return HttpResponseRedirect('/fr' + request.path)
        else:
            return HttpResponseRedirect('/en' + request.path)

        return self.get_response(request)
