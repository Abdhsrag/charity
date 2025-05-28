from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, ActivateUserView

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate'),
    path('', include(router.urls)),  
]
