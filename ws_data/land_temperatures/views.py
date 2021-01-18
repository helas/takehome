from django.db.models import Max, Min, Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

from rest_framework.views import APIView

from .models import LandTemperature
from .serializers import LandTemperatureSerializer
from .serializers import LandTemperatureUpdateAvgTemperature
from .serializers import LandTemperatureUpdateTemperatureUncertainty
from .serializers import LandTemperatureUpdateAverageUncertainty


def __get_aggregation_function_for_land_temperature_list_by_range(aggregation):
    if aggregation == 'max':
        return Max
    elif aggregation == 'min':
        return Min

    return None

class LandTemperatureList(APIView):

    def __get_aggregation_function_for_land_temperature_list_by_range(self, aggregation):
        if aggregation == 'max':
            return Max
        elif aggregation == 'min':
            return Min

        return None

    def get(self, request, format=None):
        """
        ...

        ---
        parameters:
        - name: body
          description: JSON object containing two strings: password and username.
          required: true
          paramType: body
          pytype: RequestSerializer
        """

        try:
            n_results = int(request.query_params.get('n_results'))
            start_date = datetime.strptime(request.query_params.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(request.query_params.get('end_date'), '%Y-%m-%d')
            aggregation = request.query_params.get('aggregation')

            aggregate_function = self.__get_aggregation_function_for_land_temperature_list_by_range(aggregation)
            if aggregate_function is None:
                return Response('Aggregate function can only be max or min', status=status.HTTP_400_BAD_REQUEST)

            agg_temperatures = LandTemperature.objects.filter(date__range=(start_date, end_date))\
                                                      .values('city_name')\
                                                      .order_by('city_name')\
                                                      .annotate(aggregate_function('avg_temp'))

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

    def post(self, request, format=None):
        serializer = LandTemperatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def land_temperature_list(request):
#     if request.method == 'GET':
#         try:
#             n_results = int(request.query_params.get('n_results'))
#             start_date = datetime.strptime(request.query_params.get('start_date'), '%Y-%m-%d')
#             end_date = datetime.strptime(request.query_params.get('end_date'), '%Y-%m-%d')
#             aggregation = request.query_params.get('aggregation')
#
#             aggregate_function = __get_aggregation_function_for_land_temperature_list_by_range(aggregation)
#             if aggregate_function is None:
#                 return Response('Aggregate function can only be max or min', status=status.HTTP_400_BAD_REQUEST)
#
#             agg_temperatures = LandTemperature.objects.filter(date__range=(start_date, end_date))\
#                                                       .values('city_name')\
#                                                       .order_by('city_name')\
#                                                       .annotate(aggregate_function('avg_temp'))
#
#             result = []
#             for record in agg_temperatures:
#                 city_name, agg_temp = list(record.values())
#                 result += LandTemperature.objects.filter(avg_temp=agg_temp, city_name=city_name)[:n_results]
#
#
#             serializer = LandTemperatureSerializer(result, many=True)
#             return Response(serializer.data)
#
#         except KeyError as _:
#             Response(f'Query parameters are missing', status=status.HTTP_400_BAD_REQUEST)
#
#         except Exception as error:
#             print(error)
#             return Response('Error while performing get on land_temperature-list', status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'POST':
#         serializer = LandTemperatureSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get_land_temperature_record(self, city_name, date):
        try:
            return LandTemperature.objects.get(city_name=city_name, date=date)
        except LandTemperature.DoesNotExist:
            return None

    def put(self, request, city_name, date, format=None):
        land_temperature_record = self.get_land_temperature_record(city_name, date)
        if land_temperature_record is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.__get_right_serializer_for_land_temperature_detail(request, land_temperature_record)
        if serializer is None:
            return Response('Temperature and uncertainty values missing', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def __get_right_serializer_for_land_temperature_detail(self, request, land_temperature_record):
#     avg_temp = request.data.get('avg_temp', None)
#     temp_uncertainty = request.data.get('temp_uncertainty', None)
#
#     if avg_temp is None and temp_uncertainty is None:
#         return None
#     elif avg_temp is not None and temp_uncertainty is None:
#         return LandTemperatureUpdateAvgTemperature(land_temperature_record, data=request.data)
#     elif avg_temp is None and temp_uncertainty is not None:
#         return LandTemperatureUpdateTemperatureUncertainty(land_temperature_record, data=request.data)
#
#     return LandTemperatureUpdateAverageUncertainty(land_temperature_record, data=request.data)
#
# @api_view(['GET', 'PUT'])
# def land_temperature_detail(request, city_name, date):
#     try:
#         land_temperature_record = LandTemperature.objects.get(city_name=city_name, date=date)
#     except LandTemperature.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = LandTemperatureSerializer(land_temperature_record)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = __get_right_serializer_for_land_temperature_detail(request, land_temperature_record)
#         if serializer is None:
#             return Response('Temperature and uncertainty values missing', status=status.HTTP_400_BAD_REQUEST)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#

