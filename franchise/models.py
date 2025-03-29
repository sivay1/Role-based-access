from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Report(models.Model):
    REPORT_TYPES = [
        ('Sales', 'Sales'),
        ('Inventory', 'Inventory'),
        ('Delivery Stats', 'Delivery Stats'),
    ]
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    generated_date = models.DateField()
    data = models.JSONField()

    def __str__(self):
        return f"{self.report_type} Report"
    

