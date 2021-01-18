from django.urls import path
from . import views

urlpatterns = [
    path('land_temperatures/', views.LandTemperatureList.as_view(), name='land_temperatures-list'),
    path('land_temperature/<str:city_name>/<str:date>',
         views.LandTemperatureDetail.as_view(), name='land_temperatures-detail'),

]

# not necessary because I consider only json is used
# urlpatterns = format_suffix_patterns(urlpatterns)
