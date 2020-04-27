import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from app import app      

#Read in dataset
df = pd.read_csv('https://raw.githubusercontent.com/Petrichor12/Coronavirus/master/Data/timeseries.csv')
mcases = df['Cases'].max()
mdeaths = df['Deaths'].max()
mnewcases = df['New Cases'].max()

countries = ['USA', 'China', 'S', 'Norway', 'Germany', 'Italy', 'Australia', 'Turkey']
 
#Create graph
fig = px.scatter(df[df['Country'].isin(countries)], x="Cases", y="Deaths", animation_frame="Day0",
           size="Daily Deaths", color="Country", hover_name="Country",animation_group="Country",text="Country",
                 range_x=[0,mcases], range_y=[0,mdeaths])
fig.update_layout(title='Evolution of Deaths and Cases by Country over Time')

#Layout    
page_animation =  html.Div(children=[

    dbc.Card([
        dcc.Graph(id='scatter_animation', figure=fig)
    ],
    style={'border':'0px', 'box-shadow': 'none'})
])


