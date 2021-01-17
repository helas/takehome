from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import LandTemperature


class LandTemperatureTestsWithFixtures(APITestCase):
    fixtures = ['land_temperatures.json']

    def test_land_temperatures_list(self):
        """
        Ensure we can access a list of land_temperatures when DB has 3 entries (from fixtures)
        """
        url = reverse('land_temperatures-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_land_temperatures_add(self):
        url = reverse('land_temperatures-list')
        data = {'date': "1805-04-01", 'city_name': "Racoon City", 'country_name': "USA", 'avg_temp': -13.0,
                'temp_uncertainty': 4.063, 'latitude': "1N", 'longitude': "2L"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LandTemperature.objects.count(), 4)


class LandTemperatureTestsWithoutFixtures(APITestCase):
    def test_view_land_temperatures_list(self):
        """
        Ensure we can access a list of land_temperatures when DB is empty
        """
        url = reverse('land_temperatures-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_land_temperatures_add(self):
        url = reverse('land_temperatures-list')
        data = {'date': "1805-04-01", 'city_name': "Racoon City", 'country_name': "USA", 'avg_temp': -13.0,
                'temp_uncertainty': 4.063, 'latitude': "1N", 'longitude': "2L"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LandTemperature.objects.count(), 1)
        self.assertEqual(LandTemperature.objects.get().city_name, 'Racoon City')
