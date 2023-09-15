from django.contrib import admin

# Register your models here.
from .models import Region, Parameter, WeatherData

admin.site.register(Region)
admin.site.register(Parameter)
admin.site.register(WeatherData)

