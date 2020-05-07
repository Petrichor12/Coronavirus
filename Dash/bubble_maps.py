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
from style_functions import generate_slider
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

bubble_map_layout = html.Div(children=[
    dbc.Card([
        dbc.CardBody([
            html.H2('Line graphs')]),
        html.Br(),
        html.H2('Maps'),
        dbc.Row([
            html.Br(),
            dbc.Col([
                dbc.Card([
                    dcc.Tabs(id='tabs-bubble-map', value='Total cases', children=[
                        dcc.Tab(label='Total cases', value='Total cases'),
                        dcc.Tab(label='Total deaths', value='Total deaths'),
                        dcc.Tab(label='New Cases Last Week', value='New Cases Last Week'),
                        dcc.Tab(label='New Deaths Last Week', value='New Deaths Last Week')
                    ]),
                    dbc.CardBody(html.Div([
                        dbc.Col([dcc.Graph(id='bubble-map')]),
                        generate_slider(min_days, max_days, 5, max_days, 'day-slider-bubble')
                        ]),
                    )
                ])],md=8),
            dbc.Col([
                html.Br(),
                dbc.Card(
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df_table.columns],
                        data=df_table.to_dict('records'),
                        style_table={
                            'maxHeight': '500px',
                            'overflowY': 'scroll'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ],
                        style_cell={'textAlign': 'center'},
                    )
                )
            ]),
            html.Br()
        ],justify='around')
    ])
])



@app.callback(
    Output('bubble-map', 'figure'),
    [Input('day-slider-bubble', 'value'),
     Input('tabs-bubble-map', 'value')])
def update_graph_state(days, tab):
    filtered_df = df[df.Day0 == days]
    if tab == 'Total cases':
        y = filtered_df['Cases']
    elif tab == 'Total deaths':
        y = filtered_df['Deaths']
    elif tab == 'New Cases Last Week':
        y = filtered_df['New Deaths Last Week']
    elif tab == 'New Deaths Last Week':
        y = filtered_df['New Deaths Last Week']

    fig = px.scatter_geo(filtered_df, locations="Country",
                         hover_name="Country", size=y,
                         projection="natural earth", locationmode='country names')
    fig.update_geos(showcountries=True)
    fig.update_layout(title_text=tab)

    return fig
