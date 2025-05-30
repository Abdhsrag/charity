from rest_framework import viewsets
from ..models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from project_image.models import Project_image
from rate.models import Rate
from django.db.models import Avg
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
            tag_field='projecttag__tag_id__name' #projecttag__tag_id__name is for the tag field in ProjectTag model to make the search work & it's a django orm lookup
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "Search results", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='allfeatured')
    def get_active_projects(self, request):
        active_projects = Project.objects.filter(is_fetured=True)
        serializer = self.get_serializer(active_projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='fivefeatured')
    def get_featured_projects(self, request):
        featured_projects = Project.objects.filter(is_fetured=True)[:5]
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='details')
    def project_details(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)

            # مشروع مشابه بنفس التصنيف
            similar_projects = Project.objects.filter(category=project.category).exclude(pk=project.pk)
            similar_serialized = self.get_serializer(similar_projects, many=True).data

            # صور المشروع
            images = Project_image.objects.filter(project_id=project)
            images_data = [request.build_absolute_uri(image.url.url) for image in images if image.url]

            # التقييم
            average_rating = Rate.objects.filter(project_id=project).aggregate(avg=Avg('value'))['avg']
            average_rating = round(average_rating, 2) if average_rating else 0.0

            # تفاصيل المشروع
            project_data = self.get_serializer(project).data

            return Response({
                "message": "Project details retrieved successfully.",
                "project": project_data,
                "images": images_data,
                "average_rating": average_rating,
                "similar_projects": similar_serialized
            }, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
