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
    """
    The Region model to save the regions.
    """
    title = models.CharField(max_length=255)
    parsing_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Parameter(AppBaseModel):
    """
    The Parameter to save the weather parameters.
    """
    title = models.CharField(max_length=255)
    parsing_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class MonthChoices(models.IntegerChoices):
    january =  1, "January"
    february = 2, "February"
    march =  3, "March"
    april =  4, "April"
    may =  5, "May"
    june =  6, "June"
    july =  7, "July"
    august = 8 , "August"
    september =  9, "September"
    october =   10, "October"
    november = 11, "November"
    december = 12, "December"

class SeasonChoices(models.IntegerChoices):
    winter = 1, "Winter"
    spring = 2, "Spring"
    summer = 3, "Summer"
    autumn = 4, "Autumn"


class WeatherData(AppBaseModel):
    

    class RecordTypeChoices(models.IntegerChoices):
        monthly = 1, "Monthly"
        seasonal = 2, "Seasonal"
        annual = 3, "Annual"
        
    year = models.IntegerField()
    month = models.PositiveIntegerField(choices=MonthChoices.choices, null=True)
    season = models.PositiveIntegerField(choices=SeasonChoices.choices, null=True)
    record_type = models.PositiveIntegerField(choices=RecordTypeChoices.choices, default=RecordTypeChoices.monthly)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.FloatField(null=True)

    
