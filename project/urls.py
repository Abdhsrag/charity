from django.conf.urls.i18n import urlpatterns
from django.urls import path,include


urlpatterns = [
    path('api/', include('project.api.urls')),
]



