import dash
from dash import html, dash_table
from dash import dcc
from dash.dependencies import Input, Output
from food_get.ui.map import (
    create_tracks_inclusion,
    create_2022_map,
    create_historic_map,
)
from food_get.analysis.agg_metrics import tracts_metrics_df

# Citation for dash:
#   * for commands: https://dash.plotly.com/
#   * for design inspiration: https://dash.gallery/dash-forna-container/

# data prep
df = tracts_metrics_df()

create_2022_map(df, "map_2022")


# Initialize the Dash app
app = dash.Dash(__name__)


# Define header colors
def colors():
    return {
        "h1_color": "#046b99",
        "h2_color": "#981b1e",
        "font_color": "white",
        "g1_color": "#f9f9f9",
        "g2_color": "#e6e6e6",
    }


create_tracks_inclusion("map1")

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
        "Data Year": "2010",
    },
    {
        "Data Source": "Chicago Grocery Store Data",
        "Collection Method": "csv download",
        "Data Year": "2018",
    },
    {"Data Source": "USDA SNAP", "Collection Method": "API", "Data Year": "2023"},
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
                                        "The project aims to analyze food access and security within the Chicago area. The scope of this work shows how food access has changed in the city over time and provides an updated food access metric for 2022 to understand communities’ post-pandemic food access. The data underpinning the historical component of the project includes Atlas Food Access Research data from 2019, 2015, and 2010. To recreate a more recent metric, grocery store and snap locations of the City of Chicago data are paired with demographic information from the United States census. For understanding and consumption, the project findings are presented in a Dash web application containing several interactive maps.",
                                        style={"padding": "0.25in", "height": "100%"},
                                    ),
                                    dash_table.DataTable(
                                        id="data-table",
                                        columns=[
                                            {"name": col, "id": col}
                                            for col in table_data[0].keys()
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
                                        srcDoc=open("map1.html", "r").read(),
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
                                        "The Healthy Food Financing Initiative aims to address the challenge of limited access to healthy and affordable food in the United States by expanding the availability of nutritious options in underserved communities. This initiative focuses on developing grocery stores, small retailers, corner markets, and farmers' markets to improve food access. It utilizes various indicators, including distance to stores, individual-level resources such as income and vehicle availability, and neighborhood-level indicators like average income and public transportation availability, to define and address low-income and low-access areas.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "The Food Access Research Atlas, created by the Economic Research Service using ESRI ArcGIS Server technology, provides detailed maps of food access indicators for census tracts. Utilizing demarcations based on distance to the nearest supermarket and vehicle availability, the Atlas allows users to explore and compare food access dynamics at the census-tract level. Data for 2019 and 2015, derived from supermarket lists, the 2010 Decennial Census, and the American Community Survey, enable users to analyze changes over time and make informed assessments of food access in different regions. The Atlas complements the broader Food Environment Atlas, offering specific insights into food access at a more localized level.",
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
                                        srcDoc=open("folium_map.html", "r").read(),
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
                                        "Content for Recreated Metric container goes here.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "Additional details and content for Recreated Metric.",
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
                                        srcDoc=open("map_2022.html", "r").read(),
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
                                        "Content for Conclusion container goes here.",
                                        style={"padding": "0.25in"},
                                    ),
                                    html.Br(),
                                    html.P(
                                        "Additional details and content for Conclusion.",
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
                                        srcDoc=open("folium_map.html", "r").read(),
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
        for container_id in ["container1", "container2", "container3", "container4"]
    ],
    [Input("url", "pathname")],
)
def update_container_visibility(pathname):
    if pathname is None or pathname == "/":
        return False, True, True, True  # Default to container1
    return (
        pathname != "/container1",
        pathname != "/container2",
        pathname != "/container3",
        pathname != "/container4",
    )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
