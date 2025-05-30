"""
URL configuration for charity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Charity API",
      default_version='v1',
      description="Charity API documentation",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/user/', include('user.api.urls')),
    path('api/donation/', include('donations.api.urls')),
    path('api/project_tags/', include('project_tag.urls')),
    path('api/categories/', include('category.api.urls')),
    path('api/tag/', include('tag.api.urls')),
    path('api/project-images/', include('project_image.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/project-reports/', include('project_reports.api.urls')),
    path('api/comment-reports/', include('comment_reports.api.urls')),
    path('api/project/', include('project.api.urls')),
    path('api/rate/', include('rate.api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)