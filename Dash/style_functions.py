# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

def generate_radio_button(list):
    return dcc.RadioItems(
        options=[{'label': i, 'value': i} for i in list],
        value=list[0],
        labelStyle={'display': 'inline-block',
                    'padding' : 3
                    }
      
    )


