from rest_framework import serializers

from base.models import Region, WeatherData, Parameter


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ["id", "title"]


class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = ["id", "title"]


class WeatherDataSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(source='region',
                                                   queryset=Region.objects.all(), 
                                                   write_only=True)
    parameter = ParameterSerializer(read_only=True)
    parameter_id = serializers.PrimaryKeyRelatedField(source='region', 
                                                    queryset=Parameter.objects.all(), 
                                                    write_only=True)
    month_str = serializers.CharField(source = "get_month_display", read_only=True)
    season_str = serializers.CharField(source = "get_season_display", read_only=True)
    record_type_str = serializers.CharField(source = "get_record_type_display", read_only=True)

    class Meta:
        model = WeatherData
        fields = ["id","year","month", "month_str","season","season_str", "record_type", 
                  "record_type_str", "region","region_id","parameter", "parameter_id","value"]

        
