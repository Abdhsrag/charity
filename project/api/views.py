from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

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
