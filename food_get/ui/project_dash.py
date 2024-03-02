import dash
import folium
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output

from food_get.ui.map import (
    create_tracks_inclusion,
    create_2022_map,
    create_historic_map,
    create_total_map
    )
from food_get.analysis.agg_metrics import (
    tracts_metrics_df, 
    grocery_stores_df
    )

# Data prep
metrics_df = tracts_metrics_df()
grocery_df = grocery_stores_df()

# Create maps
create_tracks_inclusion("tract_map")
create_historic_map(metrics_df, "historic_map")
create_2022_map(metrics_df,grocery_df, "2022_map")
create_total_map(metrics_df, grocery_df, "total_map")

# Define colors
def colors():
    return {
        "h1_color": "#046b99",
        "h2_color": "#981b1e",
        "font_color": "white",
        "g1_color": "#f9f9f9",
        "g2_color": "#e6e6e6",
    }

# Initialize the Dash app
app = dash.Dash(__name__)

# Table data
table_data = [
    {
        "Data Source": "Atlas Metrics",
        "Collection Method": "xlsx downloads",
        "Data Year": "2010, 2015, and 2019",
    },
    {
        "Data Source": "Census Data",
        "Collection Method": "API",
        "Data Year": "2022",
    },
    {
        "Data Source": "Census Tracts",
        "Collection Method": "csv/GeoJson download",
        "Data Year": "2010"
    },
    {
        "Data Source": "Chicago Grocery Store Data",
        "Collection Method": "csv download",
        "Data Year": "2020",
    },
    {
        "Data Source": "USDA SNAP",
        "Collection Method": "API",
        "Data Year": "2023"
    },
]

# Function to generate layout
def generate_layout(table_width):
    github_link = "https://github.com/lmucciolo/food.get"
    container_style = {
        "margin-top": ".25in",
        "margin-bottom": ".25in",
        "font-family": "Helvetica, sans-serif",
    }
    header_style_second = {
        "backgroundColor": colors()["h2_color"],
        "color": colors()["font_color"],
        "padding": "10px",
        "font-family": "Helvetica, sans-serif",
        "font-size": "16px",
    }

    return html.Div(
        [
            dcc.Location(
                id="url", refresh=False
            ),  # Location component to track URL changes
            # Main Header
            html.Div(
                [
                    html.H1(
                        "Food Access in Chicago",
                        style={
                            "backgroundColor": colors()["h1_color"],
                            "color": colors()["font_color"],
                            "padding": "10px",
                            "font-family": "Helvetica, sans-serif",
                            "margin-bottom": "0px",
                        },
                    ),
                ],
                className="header",
            ),
            # Secondary Header
            html.Div(
                [
                    html.H1(
                        [
                            dcc.Link(
                                "About",
                                href="/container1",
                                style={
                                    "color": colors()["g1_color"],
                                    "margin-right": "10px",
                                },
                            ),
                            " | ",
                            dcc.Link(
                                "Historical Metric",
                                href="/container2",
                                style={"color": colors()["g1_color"]},
                            ),
                            " | ",
                            dcc.Link(
                                "Recreated Metric",
                                href="/container3",
                                style={"color": colors()["g1_color"]},
                            ),
                            " | ",
                            dcc.Link(
                                "Conclusion",
                                href="/container4",
                                style={"color": colors()["g1_color"]},
                            ),
                            " | ",
                            dcc.Link(
                                "Footnotes",
                                href="/container5",
                                style={"color": colors()["g1_color"]},
                            ),
                            " | ",
                            html.A(
                                "GitHub",
                                href=github_link,
                                style={
                                    "color": colors()["g1_color"],
                                    "margin-right": "10px",
                                },
                            ),
                        ],
                        style={**header_style_second, "margin-top": "2px"},
                    ),
                ],
                className="header",
            ),
            # Container 1
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "Project Abstract",
                                        style={
                                            "margin-bottom": "0.5em",
                                            "margin-left": "0.25in",
                                        },
                                    ),
                                    html.P(
                                        "The project aims to analyze food access and security within the Chicago area. The scope of this work shows how food access has changed in the city over time and provides an updated food access metric for 2022 to understand communities’ post-pandemic food access. ",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "The map to the right depicts the census tracts that compose Chicago. Notably, census tracts extend into the shoreline. For the recreation of the post-pandemic food access metric, the shoreline has been removed. Additionally, the 2020 census redefined tract lines. Any changes in tract definition resulted in the tract being completely dropped for our analysis.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "Map Interaction: Viewers can toggle between options to see the shoreline changes, where water is in relation to the city, and which census tracts have been dropped.",
                                        style={"padding": "0.25in"},
                                    ),
                                ],
                                style={
                                    "width": "40%",
                                    "float": "left",
                                    "background-color": colors()["g2_color"],
                                    "margin-left": "0.25in",
                                },
                            ),
                            html.Div(
                                [
                                    html.Iframe(
                                        srcDoc=open("tract_map.html", "r").read(),
                                        width="100%",
                                        height="600px",
                                        style={
                                            "margin-left": "0.25in",
                                            "margin-right": "0.25in",
                                        },
                                    )
                                ],
                                style={"width": "50%", "float": "left"},
                            ),
                        ],
                        className="main-container",
                    ),
                ],
                style=container_style,
                id="container1",
            ),
            # Container 2
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "Atlas Score",
                                        style={
                                            "margin-bottom": "0.5em",
                                            "margin-left": "0.25in",
                                        },
                                    ),
                                    html.P(
                                        "The Food Access Research Atlas, created by the Economic Research Service using ESRI ArcGIS Server technology, provides detailed maps of food access indicators for census tracts. Utilizing demarcations based on distance to the nearest supermarket and vehicle availability, the Atlas allows users to explore and compare food access dynamics at the census-tract level. Data for 2019 and 2015, derived from supermarket lists, the 2010 Decennial Census, and the American Community Survey, enable users to analyze changes over time and make informed assessments of food access in different regions. The Atlas complements the broader Food Environment Atlas, offering specific insights into food access at a more localized level.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "The map visualizes the past trends of food access in the city. The darker the color, the lower the food access. Low income is indicated by the stripped pattern. ",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "Map Interaction: Viewers can toggle between options to switch between historical years.",
                                        style={"padding": "0.25in"},
                                    ),
                                ],
                                style={
                                    "width": "40%",
                                    "float": "left",
                                    "background-color": colors()["g2_color"],
                                    "margin-left": "0.25in",
                                },
                            ),
                            html.Div(
                                [
                                    html.Iframe(
                                        srcDoc=open("historic_map.html", "r").read(),
                                        width="100%",
                                        height="600px",
                                        style={
                                            "margin-left": "0.25in",
                                            "margin-right": "0.25in",
                                        },
                                    )
                                ],
                                style={"width": "50%", "float": "left"},
                            ),
                        ],
                        className="main-container",
                    ),
                ],
                style=container_style,
                id="container2",
                hidden=True,
            ),
            # Container 3
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "Recreated Metric",
                                        style={
                                            "margin-bottom": "0.5em",
                                            "margin-left": "0.25in",
                                        },
                                    ),
                                    html.P(
                                        "Inorder to have a post-pandemic understanding of food access in the city, our team generated new low access and low income metrics. To find the percent of a census tract that has access to a grocery store within a half mile, first the process creates ½ mile buffers around grocery stores in Chicago. These buffer boundaries are then overlaid with census tract boundaries to find the area that is not covered by the grocery store buffers (i.e., difference area). To find the ratio, or percent, of a tract that is serviced by a grocery store within a half mile radius, we take one minus the difference area over the tract area. Once each tract has an associated ratio, we classify them as low access if the ratio is less than 33%. For the low income metric, we compare each tract’s median household income to the county-wide (Cook County) median household income. If the tract’s median household income is less than or equal to 80 percent of the county's median household income, then the tract is labeled as low income.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "This map shows",
                                        style={"padding": "0.25in"},
                                    ),
                                                                        html.Br(),
                                    html.P(
                                        "Map interaction:",
                                        style={"padding": "0.25in"},
                                    ),
                                ],
                                style={
                                    "width": "40%",
                                    "float": "left",
                                    "background-color": colors()["g2_color"],
                                    "margin-left": "0.25in",
                                },
                            ),
                            html.Div(
                                [
                                    html.Iframe(
                                        srcDoc=open("tract_map.html", "r").read(),
                                        width="100%",
                                        height="600px",
                                        style={
                                            "margin-left": "0.25in",
                                            "margin-right": "0.25in",
                                        },
                                    )
                                ],
                                style={"width": "50%", "float": "left"},
                            ),
                        ],
                        className="main-container",
                    ),
                ],
                style=container_style,
                id="container3",
                hidden=True,
            ),
            # Container 4
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "Conclusion",
                                        style={
                                            "margin-bottom": "0.5em",
                                            "margin-left": "0.25in",
                                        },
                                    ),
                                    html.P(
                                        "The goal of this project is to understand Chicago’s historical food access and recreate the Atlas food metric with data post-pandemic to better understand a more recent food landscape in Chicago.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "This map compiles all the interactions from previous sections into one.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "Map interaction:",
                                        style={"padding": "0.25in"},
                                    ),
                                ],
                                style={
                                    "width": "40%",
                                    "float": "left",
                                    "background-color": colors()["g2_color"],
                                    "margin-left": "0.25in",
                                },
                            ),
                            html.Div(
                                [
                                    html.Iframe(
                                        srcDoc=open("tract_map.html", "r").read(),
                                        width="100%",
                                        height="600px",
                                        style={
                                            "margin-left": "0.25in",
                                            "margin-right": "0.25in",
                                        },
                                    )
                                ],
                                style={"width": "50%", "float": "left"},
                            ),
                        ],
                        className="main-container",
                    ),
                ],
                style=container_style,
                id="container4",
                hidden=True,
            ),
            # Container 5
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "Project Design Choices",
                                style={
                                    "margin-bottom": "0.8em",
                                    "margin-left": "0.25in",
                                },
                            ),
                            html.Ul([
                                html.Li([
                                    html.Strong("Years"),
                                    html.Ul([
                                        html.Li("For the recreated post-pandemic metric, census data from 2022 was used."),
                                        html.Li("For ease of data collection and alignment with the Chicago data portal, grocery store data is from 2018.")
                                    ])
                                ]),
                                html.Li([
                                    html.Strong("Chicago geography"),
                                    html.Ul([
                                        html.Li("For metric calculations, excluding the area of census tracks that are in the lake or river. Folium map provides viewers with the interactive ability to toggle between the original census tracts with the lake and without."),
                                        html.Li("The project only determines the metric for census tracts that stayed the same from 2010 to 2020.")
                                    ])
                                ]),
                                html.Li([
                                    html.Strong("Grocery store matching"),
                                    html.Ul([
                                        html.Li("Constrained matching process of grocery stores to SNAP providers to within 1000 feet of each other and share address numbers.")
                                    ])
                                ]),
                            ]),
                        ],
                        style={
                            "width": "40%",
                            "float": "left",
                            "background-color": colors()["g2_color"],
                            "margin-left": "0.25in",
                        },
                    ),
                    html.Div(
                        [
                            # Add the DataTable here
                            dash_table.DataTable(
                                id="data-table",
                                columns=[
                                    {"name": col, "id": col} for col in table_data[0].keys()
                                ],
                                data=table_data,
                                style_table={
                                    "height": "300px",
                                    "overflowY": "auto",
                                    "padding-left": "0.25in",
                                    "padding-right": "0.25in",
                                    "width": "5.5in",
                                },
                                style_cell={"textAlign": "center"},
                            ),
                        ],
                        style={"width": "50%", "float": "left"},
                    ),
                ],
                className="main-container",
                style=container_style,
                id="container5",
                hidden=True,
            ),
        ]
    )


# Set the initial width of the table
initial_table_width = "100%"

# Create the layout
app.layout = generate_layout(initial_table_width)


# Callback to update visibility based on URL pathname
@app.callback(
    [
        Output(container_id, "hidden")
        for container_id in ["container1", "container2", "container3", "container4", "container5"]
    ],
    [Input("url", "pathname")],
)
def update_container_visibility(pathname):
    if pathname is None or pathname == "/":
        return False, True, True, True, True  # Default to container1
    return (
        pathname != "/container1",
        pathname != "/container2",
        pathname != "/container3",
        pathname != "/container4",
        pathname != "/container5",
    )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
