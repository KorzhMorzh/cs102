from django.db import models

class Leaders(models.Model):
    email = models.CharField(max_length=30)
    score = models.IntegerField()

