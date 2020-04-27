import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date
import pandas as pd
from dash.dependencies import Input, Output
from app import app       

#Read in cases dataset
df = pd.read_csv('C:/Users/Jason Collis/Documents/Python Scripts/Coronavirus/Data/timeseries.csv')

fig = px.area(df, x="Day0", y='Cases', color="Country", range_x=[20,'Day0'])
fig.update_layout(title='Cases' +' by Country over Time')

#Add graph card with tabs
page_area = html.Div(children=[

    dcc.Tabs(id='tabs_area',value='Total cases',children=[
        dcc.Tab(label='Total cases',value='Total cases'),
        dcc.Tab(label='Total deaths',value='Total deaths'),
        dcc.Tab(label='New cases last week',value='New cases last week')
    ]),

    dbc.Card(
        dcc.Graph(id='graph_area')
    )
])

@app.callback(
    [Output('graph_area','figure')],
    [Input('tabs_area','value')]
)
def update_graph_brasil(tab):
    x = df['Day0']
    if tab == 'Total cases':
        y = df['Cases']
    elif tab == 'Total deaths':
        y = df['Deaths']
    elif tab == 'New cases last week':
        y = df['New Cases Last Week']

    figure = px.area(x=x, y=y, color=df["Country"], range_x=[20,'Day0'])
    figure.update_layout(title = tab +' by Country over Time')

    return dcc.Graph(figure = px.area(x=x, y=y, color=df["Country"], range_x=[20,'Day0']))

