import json
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

gmaps_json = 'dataset_google-maps-extractor_2024-05-30_12-04-37-597.json'

with open(gmaps_json, 'r') as file:
    data = json.load(file)

# Output data in the specified format
# https://mobisoftinfotech.com/tools/plot-multiple-points-on-map/
output_data = []
for item in data:
    output_data.append(f"{item['location']['lat']},{item['location']['lng']},{item.get('color','#333')},{item.get('shape','marker')},{item['title']}")

with open('output_data.txt', 'w') as file:
    for line in output_data:
        file.write(line + '\n')
# Create a GeoDataFrame with the longitude and latitude as geometry
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy([item['location']['lng'] for item in data], [item['location']['lat'] for item in data]))

# Set the Coordinate Reference System (CRS) for the GeoDataFrame
gdf.crs = 'EPSG:4326'  # WGS84 coordinate system

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

fig, ax = plt.subplots()
world[world['name'] == 'Luxembourg'].boundary.plot(ax=ax)
gdf[gdf['countryCode'] == 'LU'].plot(ax=ax, color='red', marker='o', markersize=5)
plt.title('Yoga Studio Locations in Luxembourg')
plt.show()


