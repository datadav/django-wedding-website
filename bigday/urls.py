from django.urls import re_path, include, path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from . import views


urlpatterns = [
    re_path(r'^', include('wedding.urls')),
    re_path(r'^', include('guests.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path('^accounts/', include('django.contrib.auth.urls')),
    path('informations/', views.informations, name='informations'),
    path('fr/informations/', views.fr_informations, name='fr_informations'),
    path('en/informations/', views.informations, name='en_informations'),
]

urlpatterns += i18n_patterns(
       path('', include('wedding.urls')),  # Assuming 'wedding' is your main app
       path('guests/', include('guests.urls')),
       # Add other app-specific URL patterns here
   )
