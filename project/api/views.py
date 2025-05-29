from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from project.models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_projects_by_user(self, request, user_id=None):
        projects = Project.objects.filter(user_id=user_id)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
