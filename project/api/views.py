from rest_framework import viewsets
from ..models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status




class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=False, methods=['get'], url_path='projects_latest')
    def latest_projects(self, request):
        latest_projects = Project.objects.order_by('-S_time')[:5]
        serializer = self.get_serializer(latest_projects, many=True)
        return Response(
            {"message": "Latest 5 projects retrieved successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )