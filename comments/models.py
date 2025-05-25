from django.db import models

# Create your models here.
class Comments(models.Model):
    ID = models.AutoField(primary_key=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # user_id = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True) #remove null & blank after merge
    # project_id = models.ForeignKey('project.Project', on_delete=models.CASCADE, null=True, blank=True) #remove null & blank after merge

    def __str__(self):
        return f"{self.content},{self.date}"