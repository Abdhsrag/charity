from rest_framework import viewsets
from ..models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from charity.utils.search import search_by_title_or_tag





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


    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        title = request.query_params.get('title')
        tag = request.query_params.get('tag')
        queryset = search_by_title_or_tag(
            self.get_queryset(),
            title=title,
            tag=tag,
            tag_field='projecttag__tag_id__name'
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "Search results", "data": serializer.data}, status=status.HTTP_200_OK)