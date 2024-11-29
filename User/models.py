from django.db import models
from django.contrib.auth.models import User

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
    
    
    
