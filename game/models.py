from django.db import models

# Create your models here.

class Users(models.Model):
	name = models.CharField(max_length=10)
	wins = models.IntegerField()
	losses = models.IntegerField()
	ties = models.IntegerField()

