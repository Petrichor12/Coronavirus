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


days_slider = list(range(20, 110, 5))
days_slider.sort()

min_days = days_slider[0]
max_days = days_slider[len(days_slider) - 1]

#Layout    
page_new_cases =  html.Div(children=[

    dbc.Card([
        dcc.Graph(id='graph_new_cases'),

        html.Br(),

        dcc.Slider(
            id='day-slider-a',
            min=min_days,
            max=max_days,
            value=115,
            marks={str(date): str(date) for date in days_slider},
            step=None
        ),

        html.Div([
            html.H6('Days since 20th Jan 2020 (Outbreak begins)')
        ])
    ],
    style={'border':'0px', 'box-shadow': 'none'})
])

@app.callback(
    Output('graph_new_cases', 'figure'),
    [Input('day-slider-a', 'value')]
)
def update_graph_state(days):

    filtered_df = df[df.Day0 == days]

    # Create graph
    fig = px.line(filtered_df, x="Cases", y="New Cases Last Week",
                  color="Country", hover_name="Country",
                  range_x=[500, mcases], range_y=[400, mnewcases], log_x=True, log_y=True, )
    fig.update_layout(title='Evolution of New Cases Last Week and Cases by Country over Time')

    return fig