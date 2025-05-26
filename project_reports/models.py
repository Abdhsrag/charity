from django.db import models

class ProjectReport(models.Model):
    description = models.TextField()
    date = models.DateField()
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True,
                                blank=True)  # remove null & blank after merge
    project_id = models.ForeignKey('project.Project', on_delete=models.CASCADE, null=True,
                                   blank=True)  # remove null & blank after merge

    def __str__(self):
        return f"Report {self.id}"
