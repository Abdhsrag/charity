from rest_framework import viewsets, status
from rest_framework.response import Response
from category.models import Category
from .serializers import CategorySerializer
from project.models import Project
from rest_framework.decorators import action
from project.api.serializers import ProjectSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "good", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def show(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

# get all projects by catrgory
    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        category = self.get_object()
        projects = Project.objects.filter(category_id=category)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)