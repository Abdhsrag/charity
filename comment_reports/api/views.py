from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from comment_reports.models import CommentReport
from .serializers import CommentReportSerializer
from django.db.models import Count

# List and create reports
class CommentReportListCreateView(generics.ListCreateAPIView):
    queryset = CommentReport.objects.all()
    serializer_class = CommentReportSerializer

# Retrieve, update, delete by ID
class CommentReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentReport.objects.all()
    serializer_class = CommentReportSerializer

# Get reports for a specific comment_id + count
class CommentReportsByCommentIdView(APIView):
    def get(self, request, comment_id):
        reports = CommentReport.objects.filter(comment_id=comment_id)
        serializer = CommentReportSerializer(reports, many=True)
        total = reports.count()
        return Response({
            "count": total,
            "data": serializer.data
        })
