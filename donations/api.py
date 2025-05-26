from rest_framework import viewsets
from .models import Donations
from .serializers import DonationsSerializer

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donations.objects.all()
    serializer_class = DonationsSerializer

