from base.views import WeatherDataList, WeatherDataViewset
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()

router.register('weather', WeatherDataViewset, basename='weather')

urlpatterns = router.urls

urlpatterns.append(
    path('weather-data/<int:region_id>/<int:parameter_id>/',
        WeatherDataList.as_view(), name='weather-data-list'),
)