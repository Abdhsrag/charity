from django.db import models

class ProjectTag(models.Model):
    tag_id = models.ForeignKey('tag.Tag', on_delete=models.CASCADE, null=True,
                               blank=True)  # FK to Tag
    project_id = models.ForeignKey('project.Project', on_delete=models.CASCADE, null=True, blank=True)  # FK to Project
    def __str__(self):
        return f"ProjectTag {self.id}"