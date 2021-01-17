from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import LandTemperature
from .serializers import LandTemperatureSerializer


@api_view(['GET', 'POST'])
def land_temperature_list(request):
    """
    List all code land_temperatures, or create a new snippet.
    """
    if request.method == 'GET':
        temperatures = LandTemperature.objects.all()[:10]
        serializer = LandTemperatureSerializer(temperatures, many=True)
        return Response(serializer.data)
