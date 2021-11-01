import pandas as pd
from geopy import GoogleV3
# from geopy.geocoders import ArcGIS
# from openpyxl import load_workbook
# import xlrd
# from geopy.extra.rate_limiter import RateLimiter

api_key = "AIzaSyD8aF9utL299_wtqfnLnAxeLBzNXlqE6GU"

geolocator = GoogleV3(api_key=api_key, domain="maps.googleapis.com")

# alter min_delay param if getting too many request error. May not need if using ArcGIS geocoder
geocode = geolocator.geocode  # min_delay_seconds=0.5

# Spreadsheet path
df = pd.read_csv(r'data\addresses.csv')

# check if city state column exists
if "address" in df:
    # create empty lists
    list_coordinates = []

    for index, row in df.iterrows():
        # try:
            address = row['address']
            location = geocode(address)
            lat, long = None, None
            if location is not None:
                lat = location.latitude
                long = location.longitude

            # print(address + " = " + str(lat), str(long))

            list_coordinates.append([lat, long])
        # except:
        #     print(index, address)
        #     break

df = df[:index]
df['coordinates'] = list_coordinates
print("\n-----------------------------------------------------------------------------------\n")
df.to_csv(r'data\addresses_with_coordinates.csv', index=None, header=True)
