from rest_framework import viewsets, status
from rest_framework.response import Response
from project_image.models import Project_image
from .serializers import ProjectImageSerializer

class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = Project_image.objects.all()
    serializer_class = ProjectImageSerializer

    # post
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Project image created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    # get all
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"message": "Project images retrieved successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    # get one
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"message": "Project image retrieved successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    # delete
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Project image deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )