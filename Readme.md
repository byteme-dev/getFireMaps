# Get Fire Maps

GetFireMaps uses Nasa service Active Data Fire  
https://firms.modaps.eosdis.nasa.gov/active_fire

How to work?
1. Download Shapefiles from 24h MODIS 1km
1. Save all data in Sqlite
1. We have a script to create a JSON file, that JSON file contains the quantity of fire data, coordinates, and date.
1. That process is automatic so the data fire are update every hour.
