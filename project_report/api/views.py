from rest_framework import viewsets
from project_report.models import ProjectReport
from .serializers import ProjectReportSerializer

class ProjectReportViewSet(viewsets.ModelViewSet):
    queryset = ProjectReport.objects.all()
    serializer_class = ProjectReportSerializer
