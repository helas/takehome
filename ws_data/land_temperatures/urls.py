from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('land_temperatures/', views.LandTemperatureList.as_view(), name='land_temperatures-list'),
    path('land_temperature/<str:city_name>/<str:date>',
         views.LandTemperatureDetail.as_view(), name='land_temperatures-detail'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
