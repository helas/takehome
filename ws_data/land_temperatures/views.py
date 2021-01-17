from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

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

    elif request.method == 'POST':
        serializer = LandTemperatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LandTemperaturesList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         temperatures = LandTemperature.objects.all()
#         serializer = LandTemperatureSerializer(temperatures, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = LandTemperatureSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)