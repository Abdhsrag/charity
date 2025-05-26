from rest_framework import viewsets
from tag.models import Tag
from .serializers import TagSerializer




class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer