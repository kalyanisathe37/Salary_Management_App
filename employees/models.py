from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    job_title = models.CharField(max_length=100, db_index=True)
    department = models.CharField(max_length=100)
    country = models.CharField(max_length=60, db_index=True)
    currency = models.CharField(max_length=3)   # INR, USD, EUR...
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    date_joined = models.DateField()

    def __str__(self):
        return self.full_name