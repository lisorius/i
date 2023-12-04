from django.db import models

class ModelYroslav(models.Model):
    waiting_for_password = None
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
