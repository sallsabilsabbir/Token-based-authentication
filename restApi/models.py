from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=10)  # 10 min validity



class Employee(models.Model):
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=25)
    emp_department = models.CharField(max_length=25)
    emp_salary = models.IntegerField()
    emp_Contact = models.CharField(max_length=30)
    emp_address = models.CharField(max_length=30)

    
