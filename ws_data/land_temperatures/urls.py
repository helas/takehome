from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('land_temperatures/', views.land_temperature_list, name='land_temperatures-list'),
    path('land_temperature/<str:city_name>/<str:date>',
         views.land_temperature_detail, name='land_temperatures-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
