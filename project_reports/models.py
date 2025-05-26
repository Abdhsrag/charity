from django.db import models

class ProjectReport(models.Model):
    description = models.TextField()
    date = models.DateField()
    user_id = models.IntegerField(null=True)  # temporary until merge
    project_id = models.IntegerField(null=True)  # temporary until merge

    def __str__(self):
        return f"Report {self.id}"
