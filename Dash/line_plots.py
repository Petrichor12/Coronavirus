import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
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

#Add main card
card_line = dbc.Card(id='card_line') 

#Add dropdown card
menu_line = dbc.Card([              
        dbc.CardHeader('Country'),
        dbc.CardBody(
            dcc.Dropdown(
                id='dropdown_countries',
                options=countries,
                value='Total'
            ),
        )
    ]) 

#Add graph card with tabs
page_line = html.Div(children=[

    dcc.Tabs(id='tabs_line',value='Total cases',children=[
        dcc.Tab(label='Total cases',value='Total cases'),
        dcc.Tab(label='Total deaths',value='Total deaths'),
        dcc.Tab(label='Daily cases',value='Daily cases')
    ]),

    dbc.Card(
        dcc.Graph(id='graph_line')
    )
])

@app.callback(
    [Output('graph_line','figure'),
    Output('card_line','children')],
    [Input('dropdown_countries','value'),
     Input('tabs_line','value')]
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

    #Prepare datetimes in string format for accessing correct values in dfs
    today = date.today()
    display_date = today.strftime('%d/%m/%y')
    
    index_date = df_cases.index[len(df_cases)-1]
    vorgestern = df_cases.index[len(df_cases)-2]    
    
    children = [dbc.CardHeader(
                    html.H5(['Data: '+display_date],
                        style={'color': '#666666'}            
                    )
                ),
                dbc.CardBody([
                    html.H5([f'Total Cases:{df_cases.loc[index_date,country]} {percentage(df_cases.loc[index_date,country],df_cases.loc[vorgestern,country])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Total Deaths:{df_deaths.loc[index_date,country]} {percentage(df_deaths.loc[index_date,country],df_deaths.loc[vorgestern,country])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Daily cases:{df_daily_cases.loc[index_date,country]} {percentage(df_daily_cases.loc[index_date,country],df_daily_cases.loc[vorgestern,country])}'],
                        style={'color': '#666666'})                        
                ])
                ]      
    return figure,children

