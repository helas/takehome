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

    def test_land_temperatures_avg_temp_update(self):
        params = {'date': "1805-04-01", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        modified_record = LandTemperature.objects.get(city_name=params['city_name'],
                                                     date=params['date'])
        self.assertEqual(modified_record.pk, 738)
        self.assertEqual(modified_record.avg_temp, data['avg_temp'])
        self.assertEqual(LandTemperature.objects.count(), 3)

    def test_land_temperatures_temp_uncertainty_update(self):

        params = {'date': "1805-04-01", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        modified_record = LandTemperature.objects.get(city_name=params['city_name'],
                                                     date=params['date'])
        self.assertEqual(modified_record.pk, 738)
        self.assertEqual(modified_record.temp_uncertainty, data['temp_uncertainty'])
        self.assertEqual(LandTemperature.objects.count(), 3)

    def test_land_temperatures_avg_and_uncertainty_update(self):
        params = {'date': "1805-04-01", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242, 'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        modified_record = LandTemperature.objects.get(city_name=params['city_name'],
                                                     date=params['date'])
        self.assertEqual(modified_record.pk, 738)
        self.assertEqual(modified_record.temp_uncertainty, data['temp_uncertainty'])
        self.assertEqual(modified_record.avg_temp, data['avg_temp'])
        self.assertEqual(LandTemperature.objects.count(), 3)

    def test_land_temperatures_update_400_when_missing_update_values(self):
        params = {'date': "1805-04-01", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        unmodified_record = LandTemperature.objects.get(city_name=params['city_name'],
                                                      date=params['date'])
        self.assertEqual(unmodified_record.pk, 738)
        self.assertEqual(unmodified_record.temp_uncertainty, 4.063)
        self.assertEqual(unmodified_record.avg_temp, 4.67)
        self.assertEqual(LandTemperature.objects.count(), 3)


    def test_land_temperatures_update_should_return_404_if_bad_city_name(self):
        params = {'date': "1805-04-01", 'city_name': "blablabla"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242, 'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_land_temperatures_update_should_return_404_if_bad_date(self):
        params = {'date': "1805-04-22", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242, 'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class LandTemperatureTestsEmptyDB(APITestCase):
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

    def test_land_temperatures_update_should_return_404_in_empty_DB(self):
        params = {'date': "1805-04-01", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242, 'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)