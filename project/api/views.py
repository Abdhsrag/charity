from rest_framework import viewsets
from project.models import Project
from rest_framework.decorators import action
from rest_framework.response import Response
from project.models import Project
from .serializers import ProjectSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
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


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from project.models import Project
from donations.models import Donations
from project.api.serializers import ProjectSerializer
from tag.models import Tag
from project_tag.models import ProjectTag

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_projects_by_user(self, request, user_id=None):
        projects = Project.objects.filter(user_id=user_id)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


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

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_project(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)

        if project.owner != request.user:
            return Response({"error": "You are not the owner"}, status=status.HTTP_403_FORBIDDEN)

        total_donation = Donations.objects.filter(project=project).aggregate(total=Sum('amount'))['total'] or 0
        donation_percentage = (total_donation / project.total_target) * 100

        if donation_percentage >= 25:
            return Response({"error": "Project cannot be canceled it is receiving 25% or more"}, status=status.HTTP_400_BAD_REQUEST)

        project.is_cancled = True
        project.save()

        return Response({"message": "Project is canceled"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='is_featured')
    def featured_project(self, request):
        featured = Project.objects.filter(is_featured=True, status='running')
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='searchtag')
    def searchtag(self, request):
        tag_name = request.query_params.get('tag')
        if not tag_name:
            return Response({"error": "tag_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tag = Tag.objects.get(name__iexact=tag_name)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

        project_ids = ProjectTag.objects.filter(tag_id=tag).values_list('project_id', flat=True)
        projects = Project.objects.filter(id__in=project_ids)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
