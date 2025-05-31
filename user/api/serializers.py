from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for general user model usage."""
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'state': {'read_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Includes password validation and confirmation.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'fname', 'lname', 'email', 'mphone',
            'password', 'confirm_password',
            'type', 'bdate', 'facebook_url', 'country',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Authenticates based on email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("Account is not activated.")
        attrs['user'] = user
        return attrs


class RequestPasswordResetSerializer(serializers.Serializer):
    """
    Serializer to request a password reset link.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer to set a new password after reset.
    """
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        return attrs
