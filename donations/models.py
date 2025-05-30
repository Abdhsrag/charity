from django.db import models

class Donations(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
                return f"Donation {self.amount} by {self.user} to {self.project}"

