from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project_image.api.views import ProjectImageViewSet

router = DefaultRouter()
router.register(r'', ProjectImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]