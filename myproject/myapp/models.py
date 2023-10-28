from django.db import models
# Create your models here.

class Restaurant_DB(models.Model):
  name = models.CharField(max_length=255)
  rating = models.FloatField()
  address = models.CharField(max_length=500)
  delivery = models.CharField(max_length=255)
  cuisine = models.CharField(max_length=255)

