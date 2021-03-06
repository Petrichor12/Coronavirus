from typing import List, Any

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
from app import app
from style_functions import generate_radio_button, generate_slider

# Read in dataset
df = pd.read_csv('https://raw.githubusercontent.com/Petrichor12/Coronavirus/master/Data/timeseries.csv')
mcases = df['Cases'].max()
mdeaths = df['Deaths'].max()
mdays = df['Day0'].max()

days_slider = list(range(20, mdays, 5))
days_slider.sort()

min_days = days_slider[0]
max_days = days_slider[len(days_slider) - 1]

# Layout
page_scatter_slider = html.Div(children=[

    html.Div([
        generate_radio_button(['Log', 'Linear'], 'axis-type-slider')
    ],
        style={'text-align': 'center', 'display': 'inline-block'}
    ),

    dbc.Card([
        dcc.Graph(id='graph_states_slider'),

        html.Br(),

        generate_slider(min_days, max_days, 5, max_days, 'day-slider'),

        html.Div([
            html.H6('Days since 1st Jan 2020')
        ], style={'text-align': 'center', 'padding':'10px'})
    ],
        style={'border': '0px', 'box-shadow': 'none'})
])

@app.callback(
    Output('graph_states_slider', 'figure'),
    [Input('axis-type-slider', 'value'),
     Input('day-slider', 'value')])
def update_graph_state(axis, days):

    filtered_df = df[df.Day0 == days]

    return {
        'data': [dict(
            x=filtered_df['Cases'],
            y=filtered_df['Deaths'],
            mode='markers',
            marker={
                'size': 14,
                'opacity': 0.7,
                'line': {'width': 1.5, 'color': 'black'}
            },
            text=filtered_df['Country']
        )],
        'layout': dict(
            xaxis={
                'type': 'linear' if axis == 'Linear' else 'log',
                'title': 'Total cases'
            },
            yaxis={
                'type': 'linear' if axis == 'Linear' else 'log',
                'title': 'Total deaths'
            },
            hovermode='closest',
            title='Total cases vs Total deaths',
            margin={'l': 70, 'b': 40, 't': 50, 'r': 30},
            hoverlabel=dict(
                font_size=16
            ),
            transition={
                'duration': 500,
                'easing' : 'cubic-in-out',
                'ordering' : 'traces first'
            }
        )
    }
