from django.db import models

# Create your models here.

class AppBaseModel(models.Model):
    """
    The base model for every model.
    Make sure you inherit this while making models except User related models.
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Region(AppBaseModel):
    title = models.CharField(max_length=255)
    parsing_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Parameter(AppBaseModel):
    title = models.CharField(max_length=255)
    parsing_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class WeatherData(AppBaseModel):
    year = models.IntegerField()
    month = models.CharField(max_length=3)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.FloatField()


    