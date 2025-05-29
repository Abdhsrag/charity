from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from user.models import User
from user.api.serializers import UserSerializer, RegisterSerializer
from user.tasks import send_verification_email

import secrets
from rest_framework import generics
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from user.tasks import send_verification_email
from user.models import User
from user.api.serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.api.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# List/Create/Update users 
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = secrets.token_urlsafe(20)  

        send_verification_email.delay(user.Email, uid, token)

class ActivateUserView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid activation link."}, status=400)

        user.is_active = True
        user.save()
        return Response({"detail": "Account activated successfully."})
# user/api/views.py



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)