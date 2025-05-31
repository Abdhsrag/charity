from rest_framework import viewsets
from donations.models import Donations
from donations.api.serializers import DonationsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donations.objects.all()
    serializer_class = DonationsSerializer

    @action(detail=False, methods=['get'], url_path='by-project/(?P<project_id>[^/.]+)')
    def donations_by_project(self, request, project_id=None):
        donations = Donations.objects.filter(project_id=project_id)
        serializer = self.get_serializer(donations, many=True)
        return Response(serializer.data)