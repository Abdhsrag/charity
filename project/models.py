from django.db import models
from category.models import Category
from user.models import User


# Create your models here.
class Project(models.Model):
    title=models.CharField(max_length=50)
    details=models.TextField()
    target=models.CharField(max_length=50)
    S_time=models.DateTimeField(auto_now_add=True)
    E_time=models.DateField()
    category_id=models.ForeignKey(Category, on_delete=models.CASCADE,blank=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,blank=True)

    is_featured=models.BooleanField(default=False)
    is_cancle=models.BooleanField(default=False)


    def __str__(self):
        return f"{self.title}-{self.details}"


