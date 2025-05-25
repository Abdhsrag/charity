from django.db import models
# from category.models import*
# from user.models import *
# Create your models here.
class Project(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=50)
    details=models.TextField()
    category=models.CharField(max_length=50)
    target=models.CharField(max_length=50)
    S_time=models.DateTimeField()
    E_time=models.DateTimeField()
    category_id=models.IntegerField(null=True)
    user_id=models.IntegerField(null=True)



    def __str__(self):
        return f"{self.title}-{self.details}"


