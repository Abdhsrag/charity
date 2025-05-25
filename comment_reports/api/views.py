from rest_framework import viewsets
from comment_reports.models import CommentReport
from .serializers import CommentReportSerializer

class CommentReportViewSet(viewsets.ModelViewSet):
    queryset = CommentReport.objects.all()
    serializer_class = CommentReportSerializer
