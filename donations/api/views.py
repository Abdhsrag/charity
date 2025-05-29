from rest_framework import viewsets
from ..models import Donations
from .serializers import DonationsSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donations.objects.all()
    serializer_class = DonationsSerializer

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_donations_by_user(self, request, user_id=None):
        donations = Donations.objects.filter(user=user_id)
        serializer = self.get_serializer(donations, many=True)
        return Response(serializer.data)
