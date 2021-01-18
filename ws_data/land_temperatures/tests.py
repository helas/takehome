from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import LandTemperature


class LandTemperatureTestsWithFixtures(APITestCase):
    fixtures = ['land_temperatures.json']

    def setUp(self):
        self.initial_number_of_records = LandTemperature.objects.count()

    def test_land_temperatures_add(self):
        """
        Ensure we can add a new land temperature record to a DB containing fixture entries
        """
        url = reverse('land_temperatures-list')
        data = {'date': "1805-04-01", 'city_name': "Racoon City", 'country_name': "USA", 'avg_temp': -13.0,
                'temp_uncertainty': 4.063, 'latitude': "1N", 'longitude': "2L"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LandTemperature.objects.count(), self.initial_number_of_records + 1)

    def test_land_temperatures_avg_temp_update(self):
        """
        Ensure it is possible to update the temperature a record of a DB containing fixture entries
        """
        params = {'date': "1805-04-01", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        modified_record = LandTemperature.objects.get(city_name=params['city_name'],
                                                     date=params['date'])
        self.assertEqual(modified_record.pk, 738)
        self.assertEqual(modified_record.avg_temp, data['avg_temp'])
        self.assertEqual(LandTemperature.objects.count(), self.initial_number_of_records)

    def test_land_temperatures_temp_uncertainty_update(self):
        """
        Ensure it is possible to update the uncertainty a record of a DB containing fixture entries
        """
        params = {'date': "1805-04-01", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        modified_record = LandTemperature.objects.get(city_name=params['city_name'],
                                                     date=params['date'])
        self.assertEqual(modified_record.pk, 738)
        self.assertEqual(modified_record.temp_uncertainty, data['temp_uncertainty'])
        self.assertEqual(LandTemperature.objects.count(), self.initial_number_of_records)

    def test_land_temperatures_avg_and_uncertainty_update(self):
        """
        Ensure it is possible to update both temp and uncertainty a record of a DB containing fixture entries
        """
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
        self.assertEqual(LandTemperature.objects.count(), self.initial_number_of_records)

    def test_land_temperatures_update_400_when_missing_update_values(self):
        """
        Ensure code 400 for update with missing update values a record of a DB containing fixture entries
        """
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
        self.assertEqual(LandTemperature.objects.count(), self.initial_number_of_records)

    def test_land_temperatures_update_should_return_404_if_bad_city_name(self):
        """
        Ensure code 404 for update with bad city name in DB containing fixture entries
        """
        params = {'date': "1805-04-01", 'city_name': "City Z"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242, 'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_land_temperatures_update_should_return_404_if_bad_date(self):
        """
        Ensure code 404 for update with bad date in DB containing fixture entries
        """
        params = {'date': "1805-04-22", 'city_name': "Århus"}
        url = reverse('land_temperatures-detail', kwargs=params)
        data = {'temp_uncertainty': 42.42424242, 'avg_temp': -15.3187}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_land_temperatures_get_group_by_city_max_agg(self):
        """
        Ensure max agg w/ group by city return right number of results in DB containing fixture entries
        """
        params = {'start_date': '1805-04-01',
                  'end_date': '1806-04-01', 'aggregation': 'max',
                  'n_results': '1'}
        url = reverse('land_temperatures-list')
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([(r['city_name'], r['avg_temp']) for r in response.data],
                         [('Århus', 12.2), ('Vice City', 8.747), ('Wasteland', 12.2)])

    def test_land_temperatures_get_group_by_city_min_agg(self):
        """
        Ensure min agg w/ group by city return right number of results in DB containing fixture entries
        """
        params = {'start_date': '1805-04-01',
                  'end_date': '1806-04-01', 'aggregation': 'min',
                  'n_results': '1'}
        url = reverse('land_temperatures-list')
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([(r['city_name'], r['avg_temp']) for r in response.data],
                         [('Århus', 4.67), ('Vice City', 4.67), ('Wasteland', 12.2)])


    def test_land_temperatures_get_group_by_city_n_gt_1(self):
        """
        Ensure agg w/ group by city return right number of results in DB containing fixture entries
        """
        params = {'start_date': '1805-04-01',
                  'end_date': '2020-04-21', 'aggregation': 'max',
                  'n_results': '10'}
        url = reverse('land_temperatures-list')
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([(r['city_name'], r['avg_temp']) for r in response.data],
                         [('Århus', 12.2), ('Vice City', 8.747), ('Wasteland', 12.2), ('Wasteland', 12.2)])


    def test_land_temperatures_get_group_by_city_empty_interval(self):
        """
        Ensure agg w/ group by city return right number of results in DB containing fixture entries
        """
        params = {'start_date': '1900-04-01',
                  'end_date': '1900-04-01', 'aggregation': 'min',
                  'n_results': '1'}
        url = reverse('land_temperatures-list')
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_land_temperatures_get_group_by_city_invalid_interval(self):
        """
        Ensure agg w/ group by city return 400 with invalid interval
        results in DB containing fixture entries
        """
        params = {'start_date': '1902-04-01',
                  'end_date': '1900-04-01', 'aggregation': 'min',
                  'n_results': '1'}
        url = reverse('land_temperatures-list')
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_land_temperatures_get_group_by_city_negative_n_results(self):
        """
        Ensure agg w/ group by city return 400 with invalid n_results
        results in DB containing fixture entries
        """
        params = {'start_date': '1802-04-01',
                  'end_date': '1900-04-01', 'aggregation': 'min',
                  'n_results': '-1'}
        url = reverse('land_temperatures-list')
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_land_temperatures_get_group_by_city_n_results_0(self):
        """
        Ensure agg w/ group by city return 400 with invalid n_results
        results in DB containing fixture entries
        """
        params = {'start_date': '1802-04-01',
                  'end_date': '1900-04-01', 'aggregation': 'min',
                  'n_results': '0'}
        url = reverse('land_temperatures-list')
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
