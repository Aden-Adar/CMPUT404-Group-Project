from django.db import models


class Images(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')