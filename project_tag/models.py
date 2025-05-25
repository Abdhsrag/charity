from django.db import models

class ProjectTag(models.Model):
    tag_id = models.IntegerField()      # FK to Tag 
    project_id = models.IntegerField()  # FK to Project 

    def __str__(self):
        return f"ProjectTag {self.id}"