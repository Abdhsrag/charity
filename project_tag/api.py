from rest_framework import viewsets
from .models import ProjectTag
from .serializers import ProjectTagSerializer


class ProjectTagViewSet(viewsets.ModelViewSet):
    queryset = ProjectTag.objects.all()
    serializer_class = ProjectTagSerializer
