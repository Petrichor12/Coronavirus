import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from style_functions import generate_slider, generate_radio_button
from app import app

df = pd.read_csv('https://raw.githubusercontent.com/Petrichor12/Coronavirus/master/Data/timeseries.csv')
mcases = df['Cases'].max()
mdeaths = df['Deaths'].max()
mnewcases = df['New Cases'].max()
mdays = df['Day0'].max()

days_slider = list(range(20, mdays, 5))
days_slider.sort()

min_days = days_slider[0]
max_days = days_slider[len(days_slider) - 1]

df_table = pd.read_csv('https://raw.githubusercontent.com/Petrichor12/Coronavirus/master/Data/world_info.csv')

projections = []
for i in ['Natural Earth', 'Orthographic', 'Mercator','Stereographic','Azimuthal Equidistant', 'Azimuthal Equal Area']:
    projections.append({'label':i,'value':i})

#Add dropdown card
menu_map = dbc.Card([
        dbc.CardHeader('Map Projection'),
        dbc.CardBody(
            dcc.Dropdown(
                id='dropdown-map-type',
                options=projections,
                value='Natural Earth'
            )
        )
    ])

map_type = dbc.Card([
        dbc.CardHeader('Map Type'),
        dbc.CardBody(
            generate_radio_button(['Bubble', 'Choropleth'], 'map-type-button')
        )
    ])

#Add graph card with tabs
page_map = html.Div(children=[

    dcc.Tabs(id='tabs-map',value='Total cases',children=[
        dcc.Tab(label='Total cases',value='Total cases'),
        dcc.Tab(label='Total deaths',value='Total deaths'),
        dcc.Tab(label='New Cases Last Week',value='New Cases Last Week'),
        dcc.Tab(label='New Deaths Last Week',value='New Deaths Last Week')
    ]),

    dbc.Card([
        dcc.Graph(id='map-graph'),

        generate_slider(min_days, max_days, 5, max_days, 'day-slider-map'),

        html.Div([
            html.H6('Days since 1st Jan 2020')
        ], style={'text-align': 'center','padding':'10px'})
    ])


])




@app.callback(
    Output('map-graph', 'figure'),
    [Input('day-slider-map', 'value'),
     Input('tabs-map', 'value'),
     Input('dropdown-map-type', 'value'),
     Input('map-type-button','value')
     ])
def update_graph_state(days, tab, projection, type):
    #filter for correct time (slider)
    filtered_df = df[df.Day0 == days]

    #filter for correct tab
    if tab == 'Total cases':
        y = filtered_df['Cases']
    elif tab == 'Total deaths':
        y = filtered_df['Deaths']
    elif tab == 'New Cases Last Week':
        y = filtered_df['New Cases Last Week']
    elif tab == 'New Deaths Last Week':
        y = filtered_df['New Deaths Last Week']

    for val in y:
        val = max(val, 0)

    #choose graph type (radio)
    if type == 'Bubble':
        fig = px.scatter_geo(filtered_df, locations="Country",
                         hover_name="Country", size=y,
                         projection=projection.lower(), locationmode='country names')
    elif type == 'Choropleth':
        fig = px.choropleth(filtered_df, locations="Country",
                             hover_name="Country", color=y,
                             projection=projection.lower(), locationmode='country names')

    fig.update_geos(showcountries=True)
    fig.update_layout(title_text=tab)

    return fig
