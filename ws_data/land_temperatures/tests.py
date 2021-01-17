from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class LandTemperatureTestsWithFixtures(APITestCase):
    fixtures = ['land_temperatures.json']

    def test_view_land_temperatures_list(self):
        """
        Ensure we can access a list of land_temperatures when DB has 3 entries (from fixtures)
        """
        url = reverse('land_temperatures-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class LandTemperatureTestsWithoutFixtures(APITestCase):
    def test_view_land_temperatures_list(self):
        """
        Ensure we can access a list of land_temperatures when DB is empty
        """
        url = reverse('land_temperatures-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
