from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from user.models import User
from user.api.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    RequestPasswordResetSerializer,
    SetNewPasswordSerializer,
)
from user.tasks import send_verification_email

import secrets


from rest_framework.permissions import IsAuthenticated

from user.models import User


# Utility to generate JWT tokens with custom claims
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['email'] = user.email
    refresh['role'] = user.type
    refresh['user_id'] = user.id
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# CRUD ViewSet for Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = secrets.token_urlsafe(20)
        send_verification_email.delay(user.email, uid, token)


# Account Activation View
class ActivateUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"detail": "Account activated successfully."})
# user.api.views.py

# In views.py

class ResendActivationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({"detail": "Account is already active."}, status=status.HTTP_400_BAD_REQUEST)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = secrets.token_urlsafe(20)

            send_verification_email.delay(user.email, uid, token)

            return Response({"detail": "Activation email has been resent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Request Password Reset View
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # reset_link = f"http://127.0.0.1:8000/api/user/reset-password/{uid}/{token}/"
        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}"
        send_mail(
            subject='Reset your password',
            message=f"Click the link to reset your password:\n\n{reset_link}",
            from_email='noreply@charity.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({'detail': 'Password reset link sent to email.'}, status=status.HTTP_200_OK)


# Confirm Password Reset View
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid or expired link.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


class SoftDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            
            # Optional: check if user is deleting their own account
            if request.user != user:
                return Response({"detail": "You cannot delete another user's account."},
                                status=status.HTTP_403_FORBIDDEN)

            # Soft delete: deactivate
            user.is_active = False
            user.save()

            return Response({"detail": "Account deactivated successfully."},
                            status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)    