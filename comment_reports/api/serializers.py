from rest_framework import serializers
from comment_reports.models import CommentReport

class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = '__all__'
