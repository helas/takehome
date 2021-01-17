from rest_framework import serializers
from .models import LandTemperature


class LandTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandTemperature
        fields = ['id', 'date', 'city_name', 'country_name', 'avg_temp', 'temp_uncertainty',
                  'latitude', 'longitude']


class LandTemperatureUpdateAvgTemperature(serializers.ModelSerializer):
    class Meta:
        model = LandTemperature
        fields = ['id', 'avg_temp']


class LandTemperatureUpdateTemperatureUncertainty(serializers.ModelSerializer):
    class Meta:
        model = LandTemperature
        fields = ['id', 'temp_uncertainty']


class LandTemperatureUpdateAverageUncertainty(serializers.ModelSerializer):
    class Meta:
        model = LandTemperature
        fields = ['id', 'avg_temp', 'temp_uncertainty']

