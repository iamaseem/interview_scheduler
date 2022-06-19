from django.db import models

# Create your models here.
class Schedule(models.Model):
  name = models.CharField(max_length=50, blank=False, default='')
  email = models.CharField(max_length=60, blank=False, default='', unique=True)
  from_time = models.CharField(max_length=20, blank=False, default='')
  to_time = models.CharField(max_length=20, blank=False, default='')
  user_type = models.CharField(max_length=30, blank=False, default='')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)  