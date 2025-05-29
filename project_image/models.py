from django.db import models

# Create your models here.
class Project_image(models.Model):
    ID = models.AutoField(primary_key=True)
    url = models.ImageField(upload_to='project_images/media')
    project_id = models.ForeignKey('project.Project', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.url}"