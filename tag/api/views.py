# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Tag
from .serializers import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer