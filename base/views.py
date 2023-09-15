from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from base.serializers import WeatherDataSerializer
from .pagination import StandardResultSetPagination

from base.models import WeatherData


# Create your views here.


class WeatherDataViewset(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    pagination_class = StandardResultSetPagination
    permission_classes = (AllowAny,)
    serializer_class = WeatherDataSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['region','parameter','year']




class WeatherDataList(ListAPIView):
    serializer_class = WeatherDataSerializer

    def get_queryset(self):
        region_id = self.kwargs['region_id']
        parameter_id = self.kwargs['parameter_id']
        return WeatherData.objects.filter(region_id=region_id, parameter_id=parameter_id)