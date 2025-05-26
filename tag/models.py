from django.db import models

# Create your models here.
class Tag(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}-{self.id}"