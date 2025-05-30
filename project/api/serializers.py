from rest_framework import serializers
from project.models import Project



class ProjectSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()


    class Meta:
        model=Project
        fields=['id','title','details','image','start_date','end_date','is_featured','average_rating','total_target']


        def get_averge_rating(self,obj):
            rates=obj.rates.all()
            if rates.exists():
                total=sum([float(rate.value)for rate in rates])
                return round (total / rates.count(),2)
            return 0