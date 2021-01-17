from rest_framework import serializers
from .models import LandTemperature


class LandTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandTemperature
        fields = ['id', 'date', 'city_name', 'country_name', 'avg_temp', 'temp_uncertainty',
                  'latitude', 'longitude']
