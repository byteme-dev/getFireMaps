from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

engine = create_engine('sqlite:///2023-10-06-fire-database.db')
conn = engine.connect()

link24h = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/shapes/zips/J1_VIIRS_C2_South_America_24h.zip'
resp = urlopen(link24h)
zipfile = ZipFile(BytesIO(resp.read()))
zipfile.extractall('./shape')
gdf24h = gpd.read_file('./shape/J1_VIIRS_C2_South_America_24h.shp')

for column in gdf24h.columns:
    gdf24h[column] = gdf24h[column].astype(str)

gdf24h.to_sql(name="SouthAmerica24h", con=engine, if_exists="replace")
