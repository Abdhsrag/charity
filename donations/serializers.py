from rest_framework import serializers
from .models import Donations

class DonationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = '__all__'

