from django.db import models

class User(models.Model):
    ID = models.AutoField(primary_key=True)
    Fname = models.CharField(max_length=100)
    Lname = models.CharField(max_length=100)
    Email = models.CharField(max_length=100, unique=True)

    Mphone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='user/imgs', blank=True, null=True)
    Pass = models.CharField(max_length=100)
    TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('donor', 'Donor'),
    ]
    Type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    Bdate = models.DateField(null=True, blank=True)
    Regist_date = models.DateTimeField(auto_now_add=True)
    Facebook_url = models.TextField(default=None, null=True)
    Country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.Fname} {self.Lname}"
    @property
    def id(self):
        return self.ID
