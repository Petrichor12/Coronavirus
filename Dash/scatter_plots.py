import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
from app import app
from style_functions import generate_radio_button

#Read in dataset
df = pd.read_csv('https://raw.githubusercontent.com/Petrichor12/Coronavirus/master/Data/world_info.csv?token=AGBFZQLLRLVU7NLPL42KDHC6UVVQG')

df.columns = ['Unnamed','Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 
           'Active Cases', 'Critical cases', 'Cases per 1M', 'Deaths per 1M', 'Total Tests', 'Test per 1M']
df = df.set_index('Country')
df = df.drop(df.columns[[0]], axis=1)

df.drop(df.tail(1).index,inplace=True)        #removes total row
df.drop(df.head(1).index,inplace=True)        #removes total row    
  

#Layout    
page_scatter =  html.Div(children=[
    
    html.Div([     
            generate_radio_button(['Log', 'Linear'],'axis-type')
            ],
            style={'text-align': 'center', 'display':'inline-block'}
        ),

    dbc.Card([
        dcc.Graph(id='graph_states')

    ],
    style={'border':'0px', 'box-shadow': 'none'})
])

@app.callback(
    Output('graph_states','figure'),
    [Input('axis-type','value')]
)
def update_graph_state(axis): 
    
    return {
        'data': [dict(
            x=df["Total Cases"],
            y=df["Total Deaths"],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.7,
                'line': {'width': 0.7, 'color': 'white'}
            },
            text=df.index
        )],
        'layout': dict(
            xaxis={
                'type': 'linear' if axis == 'Linear' else 'log',
                'title':'Total cases'
            },
            yaxis={
                'type': 'linear' if axis == 'Linear' else 'log',
                'title':'Total deaths'
            },
            hovermode='closest',
            title='Total cases vs Total deaths',
            margin={'l': 70, 'b': 40, 't': 50, 'r': 30},
            hoverlabel=dict(
                font_size=16, 
            )
        )
    }


