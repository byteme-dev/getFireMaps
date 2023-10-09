import datetime
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from sqlalchemy import create_engine, text
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd
import json

class Script:
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    def __init__(self):
        self.downloadDataLast24h()
        self.convertToJson()

    def downloadDataLast24h(self):
        engine = create_engine('sqlite:///database.db')
        conn = engine.connect()
    
        url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/shapes/zips/MODIS_C6_1_Global_24h.zip'
        print("Downloading...")
        resp = urlopen(url)
        zipfile = ZipFile(BytesIO(resp.read()))
        zipfile.extractall('./shape')
        gdf24h = gpd.read_file('./shape/MODIS_C6_1_Global_24h.shp')
    
        for column in gdf24h.columns:
            gdf24h[column] = gdf24h[column].astype(str)
    
        gdf24h.to_sql(name="World24h", con=engine, if_exists="replace")

    def get_country_from_coords(self, lat, lon):
        point = Point(lon, lat)
        for idx, row in self.world.iterrows():
            if row['geometry'].contains(point):
                return row['name']
        return ""

    def convertToJson(self):
        engine = create_engine('sqlite:///database.db')
        query_string = "SELECT LATITUDE as latitude, LONGITUDE as longitude, ACQ_DATE as date FROM World24h WHERE 1"

        with engine.connect() as connection:
           result = connection.execute(text(query_string))
           data = {}
           for row in result.fetchall():
               row_dict = {}
               for key, value in zip(result.keys(), row):
                   row_dict[key] = value
               latitude = row_dict["latitude"]
               longitude = row_dict["longitude"]
               date = row_dict["date"]
               date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d-%Y")
               country = self.get_country_from_coords(latitude, longitude)

               if data.get(country) is None:
                    data[country] = {}

               if data[country].get(date) is None:
                   data[country][date] = {}
                   data[country][date] = {"confirmed": 0, "recoveries": 0, "deaths": 0}    

               data[country][date]["confirmed"] += 1
   
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)


script = Script()