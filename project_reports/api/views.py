from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from project_reports.models import ProjectReport
from .serializers import ProjectReportSerializer

# List and create project reports
class ProjectReportListCreateView(generics.ListCreateAPIView):
    queryset = ProjectReport.objects.all()
    serializer_class = ProjectReportSerializer

# Retrieve, update, delete a specific report by ID
class ProjectReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectReport.objects.all()
    serializer_class = ProjectReportSerializer

# Get all reports for a specific project_id + count
class ProjectReportsByProjectIdView(APIView):
    def get(self, request, project_id):
        reports = ProjectReport.objects.filter(project_id=project_id)
        serializer = ProjectReportSerializer(reports, many=True)
        total = reports.count()
        return Response({
            "count": total,
            "data": serializer.data
        })
