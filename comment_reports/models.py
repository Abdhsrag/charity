from django.db import models

class CommentReport(models.Model):
    description = models.TextField()
    date = models.DateField()
    user_id = models.IntegerField(null=True)  # temporary until merge
    comment_id = models.IntegerField(null=True)  # temporary until merge

    def __str__(self):
        return f"Report {self.id}"

