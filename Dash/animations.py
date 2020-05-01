import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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

    html.Div([
        html.P('Time between contacts (days)'),
        dcc.Input(id='tc-state', type='number', value=7),
        html.P('Recovery time (days)'),
        dcc.Input(id='tr-state', type='number', value=20),
        html.P('Duration (days)'),
        dcc.Input(id='duration-state', type='number', value=30),
        html.P(' Population'),
        dcc.Input(id='pop-state', type='number', value=7e5),
        html.P(' Infected at day = 0'),
        dcc.Input(id='inf-state', type='number', value=1e5),
        html.P(' Recovered at day = 0'),
        dcc.Input(id='rec-state', type='number', value=1e4),
        html.P('Death rate'),
        dcc.Input(id='death-state', type='number', value=0.05)
    ]),

    dbc.Card([
        dcc.Graph(id='model')
    ])
])

@app.callback(Output('model', 'figure'),
              [Input('tc-state', 'value'),
               Input('tr-state', 'value'),
               Input('duration-state', 'value'),
               Input('pop-state', 'value'),
               Input('inf-state', 'value'),
               Input('rec-state', 'value'),
               Input('death-state', 'value')])
def update_output(tc, tr, duration, pop, inf, rec, death_rate):

    tc = tc  # time between contacts in days
    tr = tr  # recovery time in days

    beta = 1 / tc  # contact rate in per day
    gamma = 1 / tr  # recovery rate in per day

    system = make_system(beta, gamma, duration, pop, inf, rec)
    results = run_simulation(system, update_func)

    results.reset_index(inplace=True)
    results['Deaths'] = death_rate * results['I']
    df = results.melt(id_vars='index')

    fig = px.line(df, x="index", y="value", color="variable", line_group="variable", hover_name="variable",
                  line_shape="spline", render_mode="svg")

    return fig

