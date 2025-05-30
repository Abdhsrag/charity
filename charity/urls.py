
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

urlpatterns = [
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('admin/', admin.site.urls),
    path('api/user/', include('user.api.urls')),
    path('api/donation/', include('donations.urls')),
    path('api/project_tags/', include('project_tag.urls')),
    path('api/categories/', include('category.urls')),
    path('api/tag/', include('tag.api.urls')),
    path('api/project-images/', include('project_image.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/project-reports/', include('project_reports.api.urls')),
    path('api/comment-reports/', include('comment_reports.api.urls')),
    path('api/project/', include('project.api.urls')),
    path('api/rate/', include('rate.api.urls')),
]
