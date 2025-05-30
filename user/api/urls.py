from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, ActivateUserView,LoginView
from user.api.views import RequestPasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate'),
     path('login/', LoginView.as_view(), name='login'),
     path('request-reset-password/', RequestPasswordResetView.as_view(), name='request-reset-password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('', include(router.urls)),
]
