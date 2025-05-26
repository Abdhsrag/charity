from rest_framework.routers import DefaultRouter
from .views import RateViewSet


router=DefaultRouter()
router.register(r'rate',RateViewSet)

urlpatterns=router.urls