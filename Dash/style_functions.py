# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

def generate_radio_button(list, id):
    return dcc.RadioItems(
        id = id,
        options=[{'label': i, 'value': i} for i in list],
        value=list[0],
        labelStyle={'display': 'inline-block',
                    'padding' : 3
                    }
    )

def generate_slider(min, max, steps, value, id):
    days_slider = list(range(min, max+steps, steps))

    return dcc.Slider(
         id=id,
         min = min,
         max = max,
         value = value,
         marks = {str(date): str(date) for date in days_slider},
         step = None
    )

def generate_input(type, id, value):
    return dcc.Input(
                     id=id, type=type, value=value,
                     style = {'border': '2px solid black'}
                     )