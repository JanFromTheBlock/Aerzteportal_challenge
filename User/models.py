from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=30)
    speciality = models.CharField(max_length=30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Appointment(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    
