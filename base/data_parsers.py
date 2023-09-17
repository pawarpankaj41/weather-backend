import requests
import re

from base.models import Region, Parameter, WeatherData

base_url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/"


record_type_dict = {
    "monthly" : [1,2,3,4,5,6,7,8,9,10,11,12],
    "seasonal" : [13,14,15,16],
    "annual" : [17]
}

index_to_season_map = {
    13 : 1,
    14 : 2,
    15 : 3,
    16 : 4
}

def create_regions():
    '''
    Function to create and populate the database from the defined regions_list
    '''
    regions_list = [
            {"name" :"UK", "parsing_name" : "UK"},
            {"name" : "England", "parsing_name" : "England"},
            {"name" :"Wales", "parsing_name" : "Wales"},
            {"name" :"Scotland", "parsing_name" : "Scotland"},
            {"name" :"Northern Ireland", "parsing_name" : "Northern_Ireland"},
            {"name" :"England & Wales", "parsing_name" : "England_and_Wales"},
            {"name" :"England N", "parsing_name" : "England_N"},
            {"name" :"England S", "parsing_name" : "England_S"},
            {"name" :"Scotland N", "parsing_name" : "Scotland_N"},
            {"name" :"Scotland E", "parsing_name" : "Scotland_E"},
            {"name" :"Scotland W", "parsing_name" : "Scotland_W"},
            {"name" :"England E & NE", "parsing_name" : "England_E_and_NE"},
            {"name" :"England NW/Wales N Midlands", "parsing_name" : "England_NW_and_N_Wales"},
            {"name" : "Midlands", "parsing_name" : "Midlands"},
            {"name" :"East Anglia", "parsing_name" : "East_Anglia"},
            {"name" :"England SW/Wales S", "parsing_name" : "England_SW_and_S_Wales"},
            {"name" :"England SE/Central S", "parsing_name" : "England_SE_and_Central_S"}
    ]

    for region in regions_list:
        Region.objects.get_or_create(
            title = region["name"],
            parsing_name = region["parsing_name"],
        )

def create_parameters():
    '''
    Function to create and populate the database from the defined weatehr parameters.
    ''' 
    parameters_list = [
            {"name" :"Max temp", "parsing_name" : "Tmax"},
            {"name" : "Min temp", "parsing_name" : "Tmin"},
            {"name" :"Mean temp", "parsing_name" : "Tmean"},
            {"name" :"Sunshine", "parsing_name" : "Sunshine"},
            {"name" :"Rainfall", "parsing_name" : "Rainfall"},
            {"name" :"Rain days ≥1.0mm", "parsing_name" : "Raindays1mm"},
            {"name" :"Days of air frost", "parsing_name" : "AirFrost"},
    ]


    for parameter in parameters_list:
        Parameter.objects.get_or_create(
            title = parameter["name"],
            parsing_name = parameter["parsing_name"],
        )

def load_weather_data():
    """
    Function for the load/update weather parameters and value from uk met office.
    required Region and Parameters created in the database.
    """

    regions = Region.objects.all()
    parameters = Parameter.objects.all()

    for region in regions:
        for parameter in parameters:
            try:
                request_url= f"{base_url}{parameter.parsing_name}/date/{region.parsing_name}.txt"
                response = requests.get(request_url)
                response.raise_for_status()
            except Exception as e:
                print(str(e))
                continue

            lines = response.text.splitlines()
            headers = lines[5]
            # Skip the header line and the parameter/region line
            lines = lines[6:]

            # Loop through the data lines
            for line in lines:
                values = line.split()
                
                if len(values) != 18:
                    # this condition will execute when the current year data has empty values for months and seasons
                    if parameter.title == "Sunshine":
                        values = re.split(r'\s{3,7}', line)
                        values.pop()
                    else:
                        values = re.split(r'\s{3,7}', line)

                year = values.pop(0)

                # Loop throu.gh the values with the index
                for index, value in enumerate(values, start=1):
                    value = value.strip()
                    if value == "---":
                        value = None
                    elif value == "":
                        value = None
                    else:
                        value = float(value)

                    if index in record_type_dict["monthly"]:
                        # This condition executes when the weather parameter data is for month
                        WeatherData.objects.update_or_create(
                            year=year,
                            month=index, 
                            record_type = 1,
                            parameter=parameter, 
                            region=region, 
                            defaults={"value" : value}
                            )

                    elif index in record_type_dict["seasonal"]:
                        # This condition executes when the weather parameter data is for season
                        WeatherData.objects.update_or_create(
                            year=year,
                            season=index_to_season_map[index], 
                            record_type = 2,
                            parameter=parameter, 
                            region=region, 
                            defaults={"value" : value}
                            )
                        
                    elif index in record_type_dict["annual"]:
                        # This condition executes when the weather parameter data is for an year
                        WeatherData.objects.update_or_create(
                            year=year,
                            record_type = 3,
                            parameter=parameter, 
                            region=region, 
                            defaults={"value" : value}
                            )
                    else:
                        print("index---",index)
                        continue
