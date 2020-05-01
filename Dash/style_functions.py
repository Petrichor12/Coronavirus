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

def generate_slider(days, id):
    days_slider = list(range(20, days.max(), 5))
    days_slider.sort()
    min_days = days_slider[0]
    max_days = days_slider[len(days_slider) - 1]

    return dcc.Slider(
         id=id,
         min = min_days,
         max = max_days,
         value = 115,
         marks = {str(date): str(date) for date in days_slider},
         step = None
    )
