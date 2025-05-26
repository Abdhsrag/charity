from rest_framework import serializers
from rate.models import Rate


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rate
        fields='__all__'