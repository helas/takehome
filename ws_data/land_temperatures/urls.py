from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('land_temperatures/', views.land_temperature_list, name='land_temperatures-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
