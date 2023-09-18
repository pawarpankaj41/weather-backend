import requests
import re

from base.models import Region, Parameter, WeatherData

MET_OFFICE_BASE_URL = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/"

MONTHLY, SEASONAL, ANNUAL = "monthly", "seasonal", "annual"

RECORD_TYPE_DICT = {
    MONTHLY: (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
    SEASONAL: (13, 14, 15, 16),
    ANNUAL: (17,)
}

# this represents total elements in the list fetched from the base url and split.
TOTAL_ROW_ELEMENTS_IN_LIST = sum(len(value) for value in RECORD_TYPE_DICT.values()) + 1

INDEX_TO_SEASON_MAP = {
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
            {"name" :"England NW/Wales N", "parsing_name" : "England_NW_and_N_Wales"},
            {"name" : "Midlands", "parsing_name" : "Midlands"},
            {"name" :"East Anglia", "parsing_name" : "East_Anglia"},
            {"name" :"England SW/Wales S", "parsing_name" : "England_SW_and_S_Wales"},
            {"name" :"England SE/Central S", "parsing_name" : "England_SE_and_Central_S"}
    ]

    for region in regions_list:
        try:
            Region.objects.get_or_create(
                title = region["name"],
                parsing_name = region["parsing_name"],
            )
        except Exception as e:
            print(str(e))
            continue
    print("Regions created successfully")

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
        try:
            Parameter.objects.get_or_create(
                title = parameter["name"],
                parsing_name = parameter["parsing_name"],
            )
        except Exception as e:
            print(str(e))
            continue
    print("Parameters created successfully")
    

def create_db_entry(year, index, record_type, region, parameter, value):
    # cleaning the value before saving
    value = value.strip()
    if value == "---" or value == "":
        value = None
    else:
        value = float(value)

    if record_type is not None:
        WeatherData.objects.update_or_create(
            year=year,
            month=index if record_type == 1 else None,
            season=INDEX_TO_SEASON_MAP.get(index) if record_type == 2 else None,
            record_type=record_type,
            parameter=parameter,
            region=region,
            defaults={"value": value}
        )
    else:
        print(f"Ignored value at index {index} for {region} and {parameter}")


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
                request_url= f"{MET_OFFICE_BASE_URL}{parameter.parsing_name}/date/{region.parsing_name}.txt"
                response = requests.get(request_url)
                response.raise_for_status()
            except Exception as e:
                print(str(e))
                continue

            lines = response.text.splitlines()
            # Skip the header line and the parameter/region line and capture data lines
            data_lines = lines[6:]

            # Loop through the data lines
            for line in data_lines:
                values = line.split()
                
                if len(values) != TOTAL_ROW_ELEMENTS_IN_LIST:
                    # this condition will execute when the current year data has empty values for months and seasons
                    if parameter.title in ["Sunshine","Rainfall"]:
                        '''
                        Sunshine and Rainfall has the values with the 5 chars which makes incorrect data 
                        splitting with 3 spaces for empty values, in that case splitting on minimum 
                        2 spaces and removing last element by pop because split gives on extra empty element
                        at last index
                        '''
                        values = re.split(r'\s{2,7}', line)
                        values.pop()
                    else:
                        values = re.split(r'\s{3,7}', line)

                year = values.pop(0) # popped the year value to save 

                # Loop through the values with the index
                for index, value in enumerate(values, start=1):
                    record_type = None
                    if index in RECORD_TYPE_DICT[MONTHLY]:
                        record_type = 1
                    elif index in RECORD_TYPE_DICT[SEASONAL]:
                        record_type = 2
                    elif index in RECORD_TYPE_DICT[ANNUAL]:
                        record_type = 3

                    if record_type is not None:
                        create_db_entry(year, index, record_type, region, parameter, value)
