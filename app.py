# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 09:09:47 2025

@author: pablo.maya
"""

from flask import Flask, render_template, request, jsonify
import plotly
import os
import pandas as pd
import json
import plotly.graph_objects as go




# Initialize Flask application
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variables to store optimization solution and default controls
opt_solution = {}
controls_default = {}

# Paths to data files
json_path = "data/data.json"
url_coord = 'https://docs.google.com/uc?export=download&id=1VYEnH735Tdgqe9cS4ccYV0OUxMqQpsQh'
url_dist = 'https://docs.google.com/uc?export=download&id=1Apbc_r3CWyWSVmxqWqbpaYEacbyf1wvV'
url_demand = 'https://docs.google.com/uc?export=download&id=1w0PMK36H4Aq39SAaJ8eXRU2vzHMjlWGe'

json_path = "data/data.json"
def read_file(json_path):
    # Load JSON file
    with open(json_path, "r") as file:
        data = json.load(file)
    # Convert to DataFrame
    df = pd.DataFrame(data["locations"])
    
    return df
df = read_file(json_path)

def create_map(df):
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

    return map_actors


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and update parameters.

    Returns
    -------
    json
        JSON response containing graph data and default controls.
    """
    global parameters

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # parameters = read_data(filepath, url_coord, url_dist, url_demand)
       
        return None #jsonify({'graph_json': graph_json, 'controls_default': controls_default})



@app.route('/update_graph', methods=['POST'])
def update_graph():
    """
    Update the graph based on the optimization solution.

    Returns
    -------
    json
        JSON response containing updated graph data.
    """
    global opt_solution

    
    fig = create_map(df)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

@app.route('/')
def index():
    """
    Render the main page with initial graph and controls.

    Returns
    -------
    html
        Rendered HTML template for the main page.
    """
    # fig = create_map(df)
    # graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return render_template('index.html', graph_json=graph_json)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)