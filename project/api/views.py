from rest_framework import viewsets
from project.models import Project
from .serializers import ProjectSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)