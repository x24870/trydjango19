from django.db import models

class accounts(models.Model):
    user = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
