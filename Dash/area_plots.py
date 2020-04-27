import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date
import pandas as pd
from dash.dependencies import Input, Output
from app import app       

#Read in cases dataset
df = pd.read_csv('https://raw.githubusercontent.com/Petrichor12/Coronavirus/master/Data/timeseries.csv')

#Add graph card with tabs
page_area = html.Div(children=[

    dcc.Tabs(id='tabs_area',value='Total cases',children=[
        dcc.Tab(label='Total cases',value='Total cases'),
        dcc.Tab(label='Total deaths',value='Total deaths'),
        dcc.Tab(label='New cases last week',value='New cases last week'),
        dcc.Tab(label='New deaths last week',value='New deaths last week')
    ]),

    dbc.Card(
        dcc.Graph(id='graph_area')
    )
])

@app.callback(
    Output('graph_area','figure'),
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
    elif tab == 'New deaths last week':
        y = df['New Deaths Last Week']

    figure = px.area(x=x, y=y, color=df["Country"])
    figure.update_layout(
        title = tab +' by country over time',
        xaxis_title='Days since 1st Jan 2020',
        yaxis_title=tab,
        hovermode='closest'
        )

    return figure

