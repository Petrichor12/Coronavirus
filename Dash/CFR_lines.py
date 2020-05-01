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
 
#Create graph
x=np.arange(10,mcases*10,10000)
y=np.arange(10,mdeaths*10,10000)
lethality = [0.005,0.01,0.02,0.04,0.06,0.1]
greyscale = np.flip(np.cumsum([250/len(lethality) for x in lethality]))
lgs = list(zip(lethality,greyscale))
countries = ['China','USA','Germany','Italy','UK','Turkey','Spain','France']


fig = go.Figure()

for l,gs in lgs:
    fig.add_trace(go.Scatter(x=x, y=x*l, mode='lines',
        name=str(round(l*100,1))+'%',text=str(round(l*100,0))+'%',
        marker_color='rgb({},{},{})'.format(gs,gs,gs)
                            )
                 )

for c in countries:
    fig.add_trace(go.Scatter(x=df[df['Country']==c]['Cases'],
                             y=df[df['Country']==c]['Deaths'],
                             mode='lines+markers',text=c,name=c))

fig.update_layout(title="Deaths over Cases incl. Case Fatality Rate (CFR) Iso Lines",
                  xaxis_title="Cases",
                  yaxis_title="Deaths",
                  xaxis_type="log", yaxis_type="log",
                  height=600,
                  paper_bgcolor='rgba(255,255,255)',
                  plot_bgcolor='rgba(255,255,255,0)'
                  )
fig.update_xaxes(range=[1, 6], showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black', mirror=False)
fig.update_yaxes(range=[0.4, 5], showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black', mirror=False)

#Layout    
page_CFR_lines =  html.Div(children=[

    dbc.Card([
        dcc.Graph(id='graph_CFR_lines', figure=fig)
    ],
    style={'border':'0px', 'box-shadow': 'none'})
])


