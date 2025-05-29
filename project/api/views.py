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



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

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
