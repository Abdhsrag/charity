from django.db import models
from category.models import Category
from user.models import User


# Create your models here.
class Project(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=50)
    details=models.TextField()
    category=models.CharField(max_length=50)
    target=models.CharField(max_length=50)
    S_time=models.DateTimeField()
    E_time=models.DateTimeField()
    category_id=models.ForeignKey(Category, on_delete=models.CASCADE, null=True,blank=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    is_fetured=models.BooleanField(default=False)



    def __str__(self):
        return f"{self.title}-{self.details}"


