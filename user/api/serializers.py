from rest_framework import serializers
from user.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

# For general User representation (e.g., in ViewSets)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# For registration with password validation and confirmation
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
