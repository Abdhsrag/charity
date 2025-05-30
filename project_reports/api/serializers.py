from rest_framework import serializers
from project_reports.models import ProjectReport

class ProjectReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReport
        fields = '__all__'
