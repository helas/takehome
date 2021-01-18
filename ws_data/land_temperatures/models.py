from django.db import models


class LandTemperature(models.Model):
    date = models.DateField()
    city_name = models.TextField()
    country_name = models.TextField()
    avg_temp = models.FloatField(blank=True, null=True)
    temp_uncertainty = models.FloatField(blank=True, null=True)
    latitude = models.TextField()
    longitude = models.TextField()

    class Meta:
        managed = True
        unique_together = (('city_name', 'date'),)

        # as we are using a db generated outside of django, we need to set what's the name of
        # the table use by this model
        db_table = 'land_temperature'

