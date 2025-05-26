from django.db import models
from project.models import Project
from user.models import User


# Create your models here.
class Rate(models.Model):
    id=models.IntegerField(primary_key=True)
    value=models.DecimalField(decimal_places=2,max_digits=10)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)





    def __str__(self):
        return f"{self.value}-{self.project_id}-{self.user_id}-{self.value}"