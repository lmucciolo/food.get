"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: dash.py
Authors: Stacy George
Note: 

Description:
    This file creates the framework for the dash webpage
"""
import dash
from dash import dcc, html

# create a Dash web application
app = dash.Dash(__name__)

# layout of app
app.layout = html.Div(
    children=[
        html.H1("Analyzing food access and security in Chicago"),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
