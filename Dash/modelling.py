import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from style_functions import generate_slider
from dash.dependencies import Input, Output, State
from app import app
from modsim import *


def make_system(beta, gamma, duration=2 * 365, S=7000000000, I=500000, R=123000):
    """Make a system object for the SIR model.

    beta: contact rate in days
    gamma: recovery rate in days

    returns: System object
    """
    init = State(S=S, I=I, R=R)
    init /= sum(init)

    t0 = 0
    t_end = duration

    return System(init=init, t0=t0, t_end=t_end,
                  beta=beta, gamma=gamma)


def update_func(state, t, system):
    """Update the SIR model.

    state: State with variables S, I, R
    t: time step
    system: System with beta and gamma

    returns: State object
    """
    s, i, r = state

    infected = system.beta * i * s
    recovered = system.gamma * i

    s -= infected * t
    i += (infected - recovered) * t
    r += recovered * t

    return State(S=s, I=i, R=r)


def run_simulation(system, update_func):
    """Runs a simulation of the system.

    system: System object
    update_func: function that updates state

    returns: TimeFrame
    """
    frame = TimeFrame(columns=system.init.index)
    frame.row[system.t0] = system.init

    for t in linrange(system.t0, system.t_end):
        frame.row[t + 1] = update_func(frame.row[t], t, system)

    return frame

#Layout
page_modelling =  html.Div(children=[

    dbc.Card([
        dcc.Graph(id='model')
    ],
    style={'border': '0px', 'box-shadow': 'none'})
])

page_modelling_description = html.Div([

    html.P('The Kermack-McKendrick model is an SIR (Susceptible-Infected-Removed) model that attempts'
           ' to model how the pandemic affects a population of a certain size. It is a fairly old and simple model'
           ' that has been made into more complex versions to suit individual pandemics. The model is based on '
           'three coupled non-linear ordinary differential equations for the change in people that are susceptible,'
           ' infected or removed (dead or recovered) over time:'),
    html.Img(src="https://github.com/Petrichor12/Coronavirus/blob/master/Dash/pics/eq1.PNG?raw=true",
             height=150, width = 230),
    html.Br(),
    html.P('Where δ(a) is a Dirac delta-function and the infection pressure λ(a) equals'),
    html.Img(src = 'https://github.com/Petrichor12/Coronavirus/blob/master/Dash/pics/eq2.PNG?raw=true',
             height=50, width = 200),
    html.Br(),
    html.P('More information can be found here: https://doi.org/10.1016/j.mbs.2005.07.006'),
    html.A(href='https://doi.org/10.1016/j.mbs.2005.07.006', title='Click')
])

page_modelling_equations =  html.Div([

    html.H6
])

page_sliders_modelling = html.Div([

        html.P('Time between contacts (days)'),
        generate_slider(3, 11, 2, 7, 'tc-state'),
        html.P('Recovery time (days)'),
        generate_slider(5, 30, 5, 20, 'tr-state'),
        html.P(' Population'),
        generate_slider(0, 10000000, 1000000, 5000000, 'pop-state'),
        html.P(' Infected at day = 0'),
        generate_slider(0, 3000000, 500000, 1000000, 'inf-state'),
        html.P(' Recovered at day = 0'),
        generate_slider(0, 5000000, 500000, 1000000, 'rec-state'),
        html.P('Death rate (%)'),
        generate_slider(1, 10, 1, 5, 'death-state')
    ]),

@app.callback(Output('model', 'figure'),
              [Input('tc-state', 'value'),
               Input('tr-state', 'value'),
               Input('pop-state', 'value'),
               Input('inf-state', 'value'),
               Input('rec-state', 'value'),
               Input('death-state', 'value')])
def update_output(tc, tr, pop, inf, rec, death_rate):

    tc = tc  # time between contacts in days
    tr = tr  # recovery time in days

    beta = 1 / tc  # contact rate in per day
    gamma = 1 / tr  # recovery rate in per day

    duration = 20

    system = make_system(beta, gamma, duration, pop, inf, rec)
    results = run_simulation(system, update_func)

    results.reset_index(inplace=True)
    results['Deaths'] = death_rate/100 * results['I']
    df = results.melt(id_vars='index')

    fig = px.line(df, x="index", y="value", color="variable", line_group="variable", hover_name="variable",
                  line_shape="spline", render_mode="svg")
    fig.update_layout(
                      paper_bgcolor='rgba(255,255,255)',
                      plot_bgcolor='rgba(255,255,255,0)',
                      height=500
                      )
    fig.update_xaxes(title='Time', showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black',
                     mirror=False)
    fig.update_yaxes(title='Fraction of Population', showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=2, linecolor='black',
                     mirror=False)

    return fig

