
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/donation/', include('donations.urls')),
    path('api/project_tags/', include('project_tag.urls')),
]
