from rest_framework import serializers
from project_image.models import Project_image

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_image
        fields = ['url', 'project_id']