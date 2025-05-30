from rest_framework import serializers
from user.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import check_password
  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'state': {'read_only': True}
        }


#  registration with password validation and confirmation
class RegisterSerializer(serializers.ModelSerializer):
    Pass = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'Fname', 'Lname', 'Email', 'Mphone', 'Pass', 'confirm_password',
            'Type', 'Bdate', 'Facebook_url', 'Country'
        ]

    def validate(self, attrs):
        if attrs['Pass'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # Hash the password
        validated_data['Pass'] = make_password(validated_data['Pass'])

        # Create user with inactive status
        user = User.objects.create(is_active=False, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(Email=email).first()
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("Account is not activated.")
        if not check_password(password, user.Pass):
            raise serializers.ValidationError("Invalid email or password.")

        attrs['user'] = user
        return attrs
    




class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(Email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        return attrs
    