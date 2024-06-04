import json
import pandas as pd
import plotly.graph_objects as go

gmaps_json = 'dataset_google-maps-extractor_2024-05-30_12-04-37-597.json'

with open(gmaps_json, 'r') as file:
    data = json.load(file)

df = pd.json_normalize(data)

fig = go.Figure(data=go.Scattergeo(
    lon = df['location.lng'],
    lat = df['location.lat'],
    text = df['title'],
    mode = 'markers',
    marker_color = df['totalScore'],
))

fig.update_layout(
    title = 'Yoga Studio Locations',
    geo_scope='europe',
)

fig.show()