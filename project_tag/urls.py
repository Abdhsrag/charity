from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ProjectTagViewSet

router = DefaultRouter()
router.register(r'', ProjectTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
