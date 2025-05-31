from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationsViewSet

router = DefaultRouter()
router.register(r'', DonationsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
