#coding:UTF-8
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from line_plots import page_total,card_total,menu_line
from estados import page_estados,card_estados,menu_estados
from cidades import page_cidades,card_cidades,menu_cidades
from mapa import map_layout
from app import app


links = dbc.Row(children=[
            dbc.Col(dbc.NavLink('Maps', href='/',style={'color':'#fff'})),
            dbc.Col(dbc.NavLink('Graphs', href='/graphs',style={'color':'#fff'})),
],)

navbar = dbc.Navbar(children=[
    dbc.Row([
        dbc.Col([dbc.NavbarBrand(children='Coronavirus')]),
    ]),
    dbc.NavbarToggler(id="navbar-toggler"),
    dbc.Collapse(links, id="navbar-collapse", navbar=True),
], color="dark",dark = True,className='col-md-12')

graph_layout = html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Line graphs'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_total)],md=8),
                        dbc.Col([html.Div(menu_line),html.Br(),html.Div(card_total)])
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
                        dbc.Col([html.Div(page_estados)],md=8),
                        dbc.Col([html.Div(menu_estados),html.Br(),html.Div(card_estados)])

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
                        dbc.Col([html.Div(page_cidades)],md=8),
                        dbc.Col([html.Div(menu_cidades),html.Br(),html.Div(card_cidades)])
                    ])
                ])    
            ])
        ])    
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
    elif url == '/graphs':
        return graph_layout

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