from flask import Flask, render_template, request
import folium
import json
import os
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

app = Flask(__name__)

data_folder = "data"

def load_json(filename):
    filepath = os.path.join(data_folder, filename)
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)["locations"]

datasets = {
    "Dataset 1": load_json("data1.json"),
    "Dataset 2": load_json("data2.json")
}

# dataset=datasets['Dataset 1']
# latitudes = [loc["latitude"] for loc in dataset]
# longitudes = [loc["longitude"] for loc in dataset]
# names = [loc["name"] for loc in dataset]
# a = 1

def create_map_folium(selected_dataset):
    locations = datasets[selected_dataset]
    map_center = [locations[0]["latitude"], locations[0]["longitude"]]
    folium_map = folium.Map(location=map_center, zoom_start=6)
    
    for loc in locations:
        folium.Marker(
            [loc["latitude"], loc["longitude"]],
            popup=f"{loc['name']} ({loc['material']} - {loc['value']})",
            tooltip=loc["name"]
        ).add_to(folium_map)
    
    return folium_map._repr_html_()

# Alternative implementation using Plotly


def create_map_plotly(dataset):

    # TODO: this can be simplified by creating the dataframe directly from the json
    df = pd.DataFrame(datasets[dataset])
    # Initialize the map figure
    map_actors = go.Figure()

    # Handle case where no actors are present
    if len(df) == 0:
        map_actors.add_trace(go.Scattermapbox(
            lat=[],
            lon=[],
            mode='markers',
        ))   
        return map_actors

    # Add points
    map_actors.add_trace(go.Scattermapbox(
            lat=df['latitude'],
            lon=df['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=12,
                opacity=0.8
            ),
            text=df['name'],
            textposition='top right',
            name = "collections"
        ))
    

    # Configure the layout of the map
    map_actors.update_layout(
        mapbox=dict(
            style="open-street-map",  # Use OpenStreetMap style
            center=dict(lat=6.261943611002649, lon=-75.58979925245441),  # Center on specific coordinates
            zoom=4  # Set default zoom level
        ),
        autosize=True,
        hovermode='closest',
        showlegend=True,
        height=600,  # Set map height in pixels
        width=800
    )

    return pio.to_html(map_actors, full_html=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    selected_dataset = request.form.get("dataset", "Dataset 1")
    map_html = create_map_folium(selected_dataset)
    #map_html = create_map_plotly(selected_dataset)
    return render_template("index.html", map_html=map_html, datasets=datasets.keys(), selected_dataset=selected_dataset)

if __name__ == '__main__':
    app.run(debug=True)

