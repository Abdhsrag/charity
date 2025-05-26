from rest_framework import viewsets
from ..models import  Rate
from .serializers import RateSerializer




class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer