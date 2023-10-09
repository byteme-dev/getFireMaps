from time import sleep
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine, text
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from random import randint
import json
import geopandas as gpd
from shapely.geometry import Point
import datetime

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

user_agent = 'user_me_{}'.format(randint(10000,99999))

geolocator = Nominatim(user_agent="geoapiExercises")

app = Flask(__name__)
api = Api(app)

DATABASE_URI = 'sqlite:///2023-10-06-fire-database.db'
engine = create_engine(DATABASE_URI)

class QueryAPI(Resource):
    def reverse_geocode(self, lat, lon):
        point = Point(lon, lat)
    
        for idx, row in world.iterrows():
            if row['geometry'].contains(point):
                return row['name']
        return ""

    def get_country_from_coords(self, lat, lon):
        coord = f"{lat}, {lon}"
        location = self.reverse_geocode(lat, lon)
        return location


    def get(self):
        return json.load(open("./data.json"))
        query_string = "SELECT LATITUDE as latitude, LONGITUDE as longitude, ACQ_DATE as date FROM SouthAmerica24h WHERE 1"

        #try:
        with engine.connect() as connection:
           result = connection.execute(text(query_string))
           rows = []
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
           
           return jsonify(data)
        #except Exception as e:
        #    return {"error": str(e)}, 400

api.add_resource(QueryAPI, '/query')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
