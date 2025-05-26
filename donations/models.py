from django.db import models

class Donations(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True,
                                blank=True)  # remove null & blank after merge
    project_id = models.ForeignKey('project.Project', on_delete=models.CASCADE, null=True,
                                   blank=True)  # remove null & blank after merge

    def __str__(self):
        return f"Donation {self.id}"


