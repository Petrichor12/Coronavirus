import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
from datetime import date
import pandas as pd
from dash.dependencies import Input, Output
from app import app

def percentage(today,yesterday):
    if today > yesterday:
        return '{:+.2%}'.format(today/yesterday-1)
    elif today < yesterday:
        return '{:.2%}'.format(today/yesterday-1)
    else:
        return ''        

#Read in cases dataset
df_cases = pd.read_csv('C:/Users/Jason Collis/Documents/Python Scripts/Coronavirus/Data/Stats/Cases.csv')
df_cases = df_cases.set_index('Unnamed: 0')
df_cases.index.names = ['Date']
df_cases['Total'] = df_cases.sum(axis=1)

#Read in deaths dataset
df_deaths = pd.read_csv('C:/Users/Jason Collis/Documents/Python Scripts/Coronavirus/Data/Stats/Deaths.csv')
df_deaths = df_deaths.set_index('Unnamed: 0')
df_deaths.index.names = ['Date']
df_deaths['Total'] = df_deaths.sum(axis=1)

#Read in cases dataset
df_daily_cases = pd.read_csv('C:/Users/Jason Collis/Documents/Python Scripts/Coronavirus/Data/Stats/Daily cases.csv')
df_daily_cases = df_daily_cases.set_index('Unnamed: 0')
df_daily_cases.index.names = ['Date']
df_daily_cases['Total'] = df_daily_cases.sum(axis=1)

countries = []
for i in df_cases.columns.values:
    countries.append({'label':i,'value':i})

card_total = dbc.Card(id='card_total') 

menu_line = dbc.Card([
        dbc.CardHeader('Countries'),
        dbc.CardBody(
            dcc.Dropdown(
                id='dropdown_countries',
                options=countries,
                value='Total'
            ),
        )
    ]) 

#Layout
page_total = html.Div(children=[

    dcc.Tabs(id='tabs_total',value='Total cases',children=[
        dcc.Tab(label='Total cases',value='Total cases'),
        dcc.Tab(label='Total deaths',value='Total deaths'),
        dcc.Tab(label='Daily cases',value='Daily cases')
    ]),

    dbc.Card(
        dcc.Graph(id='graph_total')
    )
])

@app.callback(
    [Output('graph_total','figure'),
    Output('card_total','children')],
    [Input('dropdown_countries','value'),
     Input('tabs_total','value')]
)
def update_graph_brasil(country, tab):
    x = df_deaths.index
    if tab == 'Total cases':
        y = df_cases.loc[:,country].to_numpy()
    elif tab == 'Total deaths':
        y = df_deaths.loc[:,country].to_numpy()
    elif tab == 'Daily cases':
        y = df_daily_cases.loc[:,country].to_numpy()
    figure = {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':tab,
            }
    }

    today = date.today()
    display_date = today.strftime('%d/%m/%y')
    children = [dbc.CardHeader(
                    html.H5(['Data:'+display_date],
                        style={'color': '#666666'}            
                    )
                ),
                dbc.CardBody([
                    html.H5([f'Total Cases:{df_cases.Total.iloc[-1]} {percentage(df_cases.Total.iloc[-1],df_cases.Total.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Total Deaths:{df_deaths.Total.iloc[-1]} {percentage(df_deaths.Total.iloc[-1],df_deaths.Total.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Daily cases:{df_daily_cases.Total.iloc[-1]} {percentage(df_daily_cases.Total.iloc[-1],df_daily_cases.Total.iloc[-2])}'],
                        style={'color': '#666666'})                        
                ])
                ]      
    return figure,children

