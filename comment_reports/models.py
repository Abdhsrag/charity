from django.db import models

class CommentReport(models.Model):
    description = models.TextField()
    date = models.DateField()
    user = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL)  # temporary until merge
    comment = models.ForeignKey('comments.Comments', null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"Report {self.id}"

