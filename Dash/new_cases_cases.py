import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from app import app      

#Read in dataset
df = pd.read_csv('https://raw.githubusercontent.com/Petrichor12/Coronavirus/master/Data/timeseries.csv')
mcases = df['Cases'].max()
mdeaths = df['Deaths'].max()
mnewcases = df['New Cases'].max()

#Create graph
fig = px.line(df, x="Cases", y="New Cases Last Week",
              color="Country", hover_name="Country",
                 range_x=[500,mcases], range_y=[400,mnewcases],log_x=True,log_y=True,)
fig.update_layout(title='Evolution of New Cases Last Week and Cases by Country over Time',
                  paper_bgcolor='rgba(255,255,255)',
                  plot_bgcolor='rgba(255,255,255,0)',
                  height=600
                  )
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black', mirror=False)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black', mirror=False)

#Layout    
page_new_cases =  html.Div(children=[

    dbc.Card([
        dcc.Graph(id='graph_new_cases', figure=fig)
    ],
    style={'border':'0px', 'box-shadow': 'none'})
])


