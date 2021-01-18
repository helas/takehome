from django.db.models import Max, Min
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime

from rest_framework.views import APIView

from .models import LandTemperature
from .serializers import LandTemperatureSerializer
from .serializers import LandTemperatureUpdateAvgTemperature
from .serializers import LandTemperatureUpdateTemperatureUncertainty
from .serializers import LandTemperatureUpdateAverageUncertainty


class LandTemperatureList(APIView):

    def get(self, request):
        """
        Issues a GET with parameters n_results, start_date, end_date, and aggregation and returns, for each city,
        n_result values of the application of aggregation function to the temperatures
        in the range defined by start_date and end_date. Returns code 200 with data in case of success,
        or 400 if query parameters are not well formed.

        - Query parameters:

            - n_results: positive integer representing the maximum number of aggregation results by city
            - start_date: date in the format '%Y-%m-%d'
            - end_date: date in the format '%Y-%m-%d'
            - aggregation: can be max or min and is applied to avg_temp
        """

        try:
            # first we get the data passed through query parameters
            n_results = int(request.query_params.get('n_results'))
            start_date = datetime.strptime(request.query_params.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(request.query_params.get('end_date'), '%Y-%m-%d')
            aggregation = request.query_params.get('aggregation')

            if n_results < 1:
                return Response('n_results must be a positive integer', status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                return Response('start_date must be less than end_date be a positive integer',
                                status=status.HTTP_400_BAD_REQUEST)

            # based on the aggregation value, get max or min function from queryset
            aggregate_function = self.__get_aggregation_function_for_land_temperature_list_by_range(aggregation)
            if aggregate_function is None:
                return Response('Aggregate function can only be max or min', status=status.HTTP_400_BAD_REQUEST)

            # first we filter by period, group by city_name and calculate the aggregation
            agg_temperatures = LandTemperature.objects.filter(date__range=(start_date, end_date))\
                                                      .values('city_name')\
                                                      .order_by('city_name')\
                                                      .annotate(aggregate_function('avg_temp'))

            # agg_temperatures has only the city name and avg_temp. to get the other columns, we need
            # to query again the db and find the first n_results records that have the same avg_temp
            # by city
            result = []
            for record in agg_temperatures:
                city_name, agg_temp = list(record.values())
                result += LandTemperature.objects.filter(avg_temp=agg_temp, city_name=city_name)[:n_results]

            serializer = LandTemperatureSerializer(result, many=True)
            return Response(serializer.data)

        except KeyError as _:
            Response(f'Query parameters are missing', status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return Response('Error while performing get on land_temperature-list', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        Issues a POST with parameters date, city_name, country_name, avg_temp, temp_uncertainty, latitude,
        longitude that will create a new land temperature in the db. Returns 200 and a Json with the
        new record, or 400 if not well formed parameters.

        - Query data parameters:
            - date: date in the format '%Y-%m-%d'
            - city_name: name of the city
            - country_name: name of the country
            - avg_temp: float value indicating the average temperature
            - temp_uncertainty: float value indicating the uncertainty of the average temperature
            - latitude: text representing a latitude
            - longitude: text representing a longitude
        """
        serializer = LandTemperatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def __get_aggregation_function_for_land_temperature_list_by_range(self, aggregation):
        if aggregation == 'max':
            return Max
        elif aggregation == 'min':
            return Min

        return None

class LandTemperatureDetail(APIView):

    def __get_right_serializer_for_land_temperature_detail(self, request, land_temperature_record):
        avg_temp = request.data.get('avg_temp', None)
        temp_uncertainty = request.data.get('temp_uncertainty', None)

        if avg_temp is None and temp_uncertainty is None:
            return None
        elif avg_temp is not None and temp_uncertainty is None:
            return LandTemperatureUpdateAvgTemperature(land_temperature_record, data=request.data)
        elif avg_temp is None and temp_uncertainty is not None:
            return LandTemperatureUpdateTemperatureUncertainty(land_temperature_record, data=request.data)

        return LandTemperatureUpdateAverageUncertainty(land_temperature_record, data=request.data)

    def put(self, request, city_name, date):
        """
        Issues a PUT with parameters city_name and date and data containing an avg_temp and/or a
        uncertainty value, and updates a record. Returns code 200 and a Json with the new record,
        or 400 in case data is not well formed or 404 if there is not a record with the given
        city_name and date.

        - Parameters:
            - date: date in the format '%Y-%m-%d'
            - city_name: name of the city

        - Post data parameters:
            - avg_temp: float value indicating the average temperature
            - temp_uncertainty: float value indicating the uncertainty of the average temperature
        """
        try:
            land_temperature_record = LandTemperature.objects.get(city_name=city_name, date=date)
        except LandTemperature.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # based on the presence of avg temp and/or uncertainty, we choose the right serializer
        serializer = self.__get_right_serializer_for_land_temperature_detail(request, land_temperature_record)
        if serializer is None:
            return Response('Temperature and uncertainty values missing', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
