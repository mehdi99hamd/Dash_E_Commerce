import base64
import datetime
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ClientsideFunction, Input, Output, State
from dash import dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import grasia_dash_components as gdc
from dash import Dash, html, Input, Output, callback_context, State
import numpy as np
import plotly.express as px
import os
from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
import plotly.graph_objs as go
from functools import partial
from datetime import date
import sys

import callbacks

external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME,
    "https://use.fontawesome.com/releases/v5.0.6/css/all.css", "https://fonts.googleapis.com/icon?family=Material+Icons+Sharp", "https://fonts.googleapis.com",
"https://fonts.gstatic.com","https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap", dbc.themes.PULSE
]

external_scripts = [
    {'src': "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.8.0/chart.min.js',
        'integrity': 'sha512-sW/w8s4RWTdFFSduOTGtk4isV1+190E/GghVffMA9XczdJ2MDzSzLEubKAs5h0wzgSJOQTRYyaz73L3d6RtJSg==',
        'crossorigin': 'anonymous',
        'referrerpolicy' : "no-referrer"
    }
]

hidden = ' hidden'

visible = ' visible'

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


port =  8050

app = dash.Dash(__name__, assets_folder=find_data_file('assets/'), external_scripts = external_scripts, 
                external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.title='Siffect DashBoard'

server = app.server

path = r'oresli.csv'
oresli = pd.read_csv(path)

oresli['Date '] = pd.to_datetime(oresli['Date '])

info_path = r'info_product.csv'
info_data = pd.read_csv(info_path, encoding='latin-1')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='data_oresli', data = oresli.values), 
    dcc.Store(id='column_oresli', data = oresli.columns),
    dcc.Store(id='info_pro', data = info_data.values), 
    dcc.Store(id='column_info', data = info_data.columns),
], className = 'body1', id = 'body')


if __name__ == '__main__':
    app.run_server(debug = True)