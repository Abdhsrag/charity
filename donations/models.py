from django.db import models

class Donations(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    project_id = models.IntegerField()  # FK to Project 
    user_id = models.IntegerField()     # FK to User 

    def __str__(self):
        return f"Donation {self.id}"


