from django.urls import path, include

urlpatterns = [
    path('api/', include('tag.api.urls')), 
]