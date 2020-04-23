import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
from app import app

#Read in dataset
df = pd.read_csv('C:/Users/Jason Collis/Documents/Python Scripts/Coronavirus/Data/world_info.csv')

df.columns = ['Unnamed','Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 
           'Active Cases', 'Critical cases', 'Cases per 1M', 'Deaths per 1M', 'Total Tests', 'Test per 1M']
df = df.set_index('Country')
df = df.drop(df.columns[[0]], axis=1)

df.drop(df.tail(1).index,inplace=True)        #removes total row
df.drop(df.head(1).index,inplace=True)        #removes total row      

#Layout    
page_scatter =  html.Div(children=[

    dbc.Card([
        dcc.RadioItems(
                id='axis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Log',
                labelStyle={'display': 'inline-block'}
            ),
        dcc.Graph(id='graph_states')
    ])
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
                'size': 10,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'type': 'linear' if axis == 'Linear' else 'log'
            },
            yaxis={
                'type': 'linear' if axis == 'Linear' else 'log'
            },
            hovermode='closest'
        )
    }


