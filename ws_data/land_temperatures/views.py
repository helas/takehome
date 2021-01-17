from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import LandTemperature
from .serializers import LandTemperatureSerializer
from .serializers import LandTemperatureUpdateAvgTemperature
from .serializers import LandTemperatureUpdateTemperatureUncertainty
from .serializers import LandTemperatureUpdateAverageUncertainty



@api_view(['GET', 'POST', 'PUT'])
def land_temperature_list(request):
    """
    List 10 first code land temperatures, or create a new land temperature.
    """
    if request.method == 'GET':
        temperatures = LandTemperature.objects.all()[:10]
        serializer = LandTemperatureSerializer(temperatures, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LandTemperatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def __get_right_serializer_for_land_temperature_detail(request, land_temperature_record):
    avg_temp = request.data.get('avg_temp', None)
    temp_uncertainty = request.data.get('temp_uncertainty', None)

    if avg_temp is None and temp_uncertainty is None:
        return None
    elif avg_temp is not None and temp_uncertainty is None:
        return LandTemperatureUpdateAvgTemperature(land_temperature_record, data=request.data)
    elif avg_temp is None and temp_uncertainty is not None:
        return LandTemperatureUpdateTemperatureUncertainty(land_temperature_record, data=request.data)

    return LandTemperatureUpdateAverageUncertainty(land_temperature_record, data=request.data)


@api_view(['GET', 'PUT'])
def land_temperature_detail(request, city_name, date):
    try:
        land_temperature_record = LandTemperature.objects.get(city_name=city_name, date=date)
    except LandTemperature.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LandTemperatureSerializer(land_temperature_record)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = __get_right_serializer_for_land_temperature_detail(request, land_temperature_record)
        if serializer is None:
            return Response('Temperature and uncertainty values missing', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



