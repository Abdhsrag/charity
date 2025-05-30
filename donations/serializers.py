from rest_framework import serializers
from donations.models import Donations

class DonationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = ['id', 'amount', 'date', 'user', 'project']
        read_only_fields = ['date']
