
from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country= models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
