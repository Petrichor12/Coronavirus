#coding:UTF-8
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from line_plots import page_line,card_line,menu_line
from scatter_plots_slider import page_scatter_slider
from area_plots import page_area
from new_cases_cases import page_new_cases
from CFR_lines import page_CFR_lines
from animations import page_modelling
from mapa import map_layout
from app import app


links = dbc.Row(children=[
            dbc.Col(dbc.NavLink('Maps', href='/',style={'color':'#fff'})),
            dbc.Col(dbc.NavLink('Basic Graphs', href='/basic-graphs',style={'color':'#fff'})),
            dbc.Col(dbc.NavLink('Advanced Graphs', href='/advanced-graphs',style={'color':'#fff'})),
            dbc.Col(dbc.NavLink('Pandemic Modelling', href='/modelling',style={'color':'#fff'})),
],)

navbar = dbc.Navbar(children=[
    dbc.Row([
        dbc.Col([dbc.NavbarBrand(children='Coronavirus')]),
    ]),
    dbc.NavbarToggler(id="navbar-toggler"),
    dbc.Collapse(links, id="navbar-collapse", navbar=True),
], color="dark", dark = True, className='col-md-12')

graph_layout = html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Line graphs'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_line)],md=8),
                        dbc.Col([html.Div(menu_line),html.Br(),html.Div(card_line)])
                    ]),
                ])    
        ]),
        html.Br(),
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Scatter plots'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_scatter_slider)],md=12)
                    ]),
                ])    
            ])
        ]),
        html.Br(),
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Area graphs'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_area)],md=12)
                    ])
                ])    
            ])
        ])    
  ])

adv_graph_layout = html.Div([
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Other plots'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_new_cases)],md=12)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_CFR_lines)],md=12)
                    ]),
                ])    
            ])
        ]),
        html.Br(),
   
  ])    

modelling_layout = html.Div([
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Kermack-McKendrick Model'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_modelling)],md=12)
                    ]),
                    html.Br(),
                    
                ])    
            ])
        ]),
        html.Br(),
   
  ])    

footer = dbc.Row([
    dbc.Col(
        [dcc.Markdown('''
                All data taken from https://www.worldometers.info/coronavirus/ 
                ''')],
        md=8
        ),
    dbc.Col(
        [dcc.Markdown('''    
            Produced by the Vat Boys
            ''')],
        width={'offset':1},
        )
])      
    
#Layout
app.layout = html.Div(children=[
    dcc.Location(id='url'),
    html.Header(children=navbar),
    html.Br(),
    dbc.Container(id='content',fluid=True),
    html.Br(),
    html.Hr(),
    dbc.Container(footer,fluid=True)                    
    ])         


@app.callback(
    Output('content','children'),
    [Input('url','pathname')]
)
def update_content(url):
    if url == '/':
        return map_layout
    elif url == '/basic-graphs':
        return graph_layout
    elif url == '/advanced-graphs':
        return adv_graph_layout
    elif url == '/modelling':
        return modelling_layout

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

server = app.server    

if __name__ == '__main__':
    app.run_server(debug=True)    