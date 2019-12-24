from django.db import models

class City(models.Model):
    """Database model for cities in the system"""
    city_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Cities'


    def __str__(self):
        """Retrieve full name of city"""
        return self.city_name
