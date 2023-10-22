import base64
import datetime
import io
from ast import Pass

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
from plotly.subplots import make_subplots
import sys

import model

path = r'oresli.csv'
oresli = pd.read_csv(path)


list_products = list(oresli['produit_Cible'].unique())
if 'None' in list_products :
    list_products.remove('None')
if '*' in list_products : 
    list_products.remove('*')

color = [
    'rgb(136, 191, 140)',     # Votre couleur de référence
    'rgb(96, 151, 100)',      # Plus sombre
    'rgb(76, 131, 80)',       # Encore plus sombre
    'rgb(116, 171, 120)',     # Un peu plus sombre
    'rgb(156, 211, 160)',     # Plus clair
    'rgb(176, 231, 180)',     # Encore plus clair
    'rgb(106, 161, 110)',     # Entre la couleur de référence et la plus sombre
    'rgb(146, 201, 150)',     # Entre la couleur de référence et la plus claire
    'rgb(66, 121, 70)',       # Très sombre
    'rgb(186, 241, 190)',     # Très clair
    'rgb(126, 181, 130)',     # Proche de la couleur de référence
    'rgb(166, 221, 170)'      # Un peu plus clair que la couleur de référence
]

color_red = ['rgb(216,24, 24)']




                    


layout = [
    html.Div([
        html.Aside([

            html.Div([
                html.Div([
                    html.Img(src = '/assets/sifect.png'),
                    #html.H2(['SIF', html.Span('FECT', className='primary')]),
                ], className='logo'),
                html.Div([
                    html.Span('close', className='material-icons-sharp')
                ], className='close', id='close-btn')
            ], className='top'),

            html.Div([
                dcc.Link([
                    html.Span('grid_view', className='material-icons-sharp'),
                    html.H3('Dashboard')
                ], href = '/'),
                dcc.Link([
                    html.Span('insights', className='material-icons-sharp'),
                    html.H3('Analytics')
                ], href = '/analysis'),
                dcc.Link([
                    html.Span('inventory', className='material-icons-sharp'),
                    html.H3('Products')
                ], href = '/products', className='active'),
                dcc.Link([
                    html.Span('category', className='material-icons-sharp'),
                    html.H3('Collection')
                ], href = '/collection'),
                dcc.Link([
                    html.Span('summarize', className='material-icons-sharp'),
                    html.H3('Report')
                ], href = '/Report'),
                dcc.Link([
                    html.Span('update', className='material-icons-sharp'),
                    html.H3('Update')
                ], href = '/update'),
            ], className='sidebar'),

        ]),
         # ---------------------- END OF ASIDE --------------------------------#
        html.Main([
            html.Div([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                html.H1("", id = 'products_title'),
                                            ], style={'textAlign': 'center'}) 
                                        ]), className = 'row_fig'
                                    ),
                                ])
                            ], width=4),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                dcc.Dropdown(
                                                    id='produits_chosen_products',
                                                    options = [{
                                                        'label': i,
                                                        'value': i
                                                    } for i in list_products],
                                                    multi=False,
                                                    value = 'epilateur',
                                                    className = 'dropdown', 
                                                    placeholder='Select Products'
                                                )
                                            ], style={'textAlign': 'center'}) 
                                        ]), className = 'row_fig'
                                    ),
                                ])
                            ], width=4),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                dcc.DatePickerRange(
                                                    minimum_nights=0,
                                                    clearable=True,
                                                    display_format = 'M/D/Y',
                                                    with_portal=True,
                                                    id="date_products",
                                                    className = 'datetime', 
                                                ),
                                            ], style={'textAlign': 'center'}) 
                                        ]), className = 'row_fig'
                                    ),
                                ])  
                            ], width=4),
                        ], align='center'), 
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                html.Div([
                                                    html.H2('Sales'),
                                                    html.H3('', id = 'sale_products'),
                                                ]),
                                                html.Div([
                                                    html.Div([ 
                                                        '{30,60,90,60,100,50,45,20}'
                                                    ], className='sparks dotline-extrathick'),
                                                    html.Small(children = [], className = 'success-2', id = 'sale_products_percentage'), 
                                                ])
                                            ], className='row_fig_content')
                                    ]), className = 'row_fig_1'
                                    ),
                                ])
                            ], width=2),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                html.Div([
                                                    html.H2('Budget'),
                                                    html.H3('', id = 'budget_products'),
                                                ]),
                                                html.Div([
                                                    html.Div([ 
                                                        '{30,60,90,60,100,50,45,20}'
                                                    ], className='sparks dotline-extrathick'),
                                                    html.Small(children = [], className = 'success-2', id = 'budget_products_percentage'), 
                                                ])
                                            ], className='row_fig_content')
                                    ]), className = 'row_fig_1'
                                    ),
                                ])
                            ], width=2),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                html.Div([
                                                    html.H2('Incomes'),
                                                    html.H3('', id = 'income_products'),
                                                ]),
                                                html.Div([
                                                    html.Div([ 
                                                        '{30,60,90,60,100,50,45,20}'
                                                    ], className='sparks dotline-extrathick'),
                                                    html.Small(children = [], className = 'danger', id = 'income_products_percentage'), 
                                                ])
                                            ], className='row_fig_content')
                                    ]), className = 'row_fig_1'
                                    ),
                                ])
                            ], width=2),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                html.Div([
                                                    html.H2('Visitors'),
                                                    html.H3('', id = 'visits_products'),
                                                ]),
                                                html.Div([
                                                    html.Div([ 
                                                        '{30,60,90,60,100,50,45,20}'
                                                    ], className='sparks bar-extrawide'),
                                                    html.Small(children = [], className = 'success-2', id = 'visits_products_percentage'), 
                                                ])
                                            ], className='row_fig_content')
                                    ]), className = 'row_fig_1'
                                    ),
                                ])
                            ], width=2),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                html.Div([
                                                    html.H2('Products'),
                                                    html.H3('', id = 'products_products'),
                                                ]),
                                                html.Div([
                                                    html.Div([ 
                                                        '{30,60,90,60,100,50,45,20}'
                                                    ], className='sparks bar-extrawide'),
                                                    html.Small(children = [], className = 'success-2', id = 'products_products_percentage'), 
                                                ])
                                            ], className='row_fig_content')
                                    ]), className = 'row_fig_1'
                                    ),
                                ])
                            ], width=2),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Div([
                                                html.Div([
                                                    html.H2('ROAS'),
                                                    html.H3('', id = 'roas_products'),
                                                ]),
                                                html.Div([
                                                    html.Div([ 
                                                        '{30,60,90,60,100,50,45,20}'
                                                    ], className='sparks bar-extrawide'),
                                                    html.Small(children = [], className = 'success-2', id = 'roas_products_percentage'), 
                                                ])
                                            ], className='row_fig_content')
                                    ]), className = 'row_fig_1'
                                    ),
                                ])
                            ], width=2),
                        ], align='center'), 
                        html.Br(),
                        # Products
                        dbc.Row([
                            dbc.Col([
                                html.Div([], className = 'info_products', id = 'info_products')
                            ], width=4),
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            dbc.Card(
                                                dbc.CardBody([
                                                    dcc.Graph(
                                                        figure=go.Figure(),
                                                        id = 'graph_products',
                                                        config={
                                                            'displayModeBar': False
                                                        }
                                                    ) 
                                                ]), className = 'row_fig'
                                            ),  
                                        ])
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            dbc.Card(
                                                dbc.CardBody([
                                                    dcc.Graph(
                                                        figure=go.Figure(),
                                                        id = 'graph_products2',
                                                        config={
                                                            'displayModeBar': False
                                                        }
                                                    ) 
                                                ]), className = 'row_fig'
                                            ),  
                                        ])
                                    ], width=6),
                                ], align='center'),
                                html.Br(), 
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            dbc.Card(
                                                dbc.CardBody([
                                                    dcc.Graph(
                                                        figure=go.Figure(),
                                                        id = 'graph_products3',
                                                        config={
                                                            'displayModeBar': False
                                                        }
                                                    ) 
                                                ]), className = 'row_fig'
                                            ),  
                                        ])
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            dbc.Card(
                                                dbc.CardBody([
                                                    dcc.Graph(
                                                        figure=go.Figure(),
                                                        id = 'graph_products4',
                                                        config={
                                                            'displayModeBar': False
                                                        }
                                                    ) 
                                                ]), className = 'row_fig'
                                            ),  
                                        ])
                                    ], width=6),
                                ], align='center'), 
                            ]),
                        ], align='center'), 
                        html.Br(), 
                        # Visit Evolution & Visit Per Product
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            dcc.Graph(
                                                figure=go.Figure(),
                                                id = 'graph_products6',
                                                config={
                                                    'displayModeBar': False
                                                }
                                            ) 
                                        ]), className = 'row_fig'
                                    ),  
                                ])
                            ], width=7),
                            dbc.Col([
                                html.Div([
                                    dbc.Card(
                                        dbc.CardBody([
                                            dcc.Graph(
                                                figure=go.Figure(),
                                                id = 'graph_products5',
                                                config={
                                                    'displayModeBar': False
                                                }
                                            ) 
                                        ]), className = 'row_fig'
                                    ),  
                                ])
                            ], width=5),
                        ], align='center'),
                    ]), className = 'fig_card' 
                )
            ], className = 'table_fig')
        ]),
        # --------------- END OF MAIN ---------------------#
        
    ], className='container_analysis')
]





