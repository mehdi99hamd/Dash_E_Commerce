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
from dash_svg import Svg, G, Path, Circle
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

import model





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
                ], href = '/', className='active'),
                dcc.Link([
                    html.Span('insights', className='material-icons-sharp'),
                    html.H3('Analytics')
                ], href = '/analysis'),
                dcc.Link([
                    html.Span('inventory', className='material-icons-sharp'),
                    html.H3('Products')
                ], href = '/products'),
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
            html.H1(['DASHBOARD E-COMMERCE : OVERVIEW ',  ], id = 'now'),

            html.Div([
                html.Div([
                    html.Span('analytics', className="material-icons-sharp span-icon"),
                    html.Div([
                        html.Div([
                            html.H3('Sales'),
                            html.H2([''], id = 'sale')
                        ], className='left'),
                        html.Div([
                            html.Div([
                                html.Span('', className='success', id = 'sale_percentage'), 
                                html.Div([
                                    html.Div([], className = 'bar success_cercle', id = 'sale_cercle_bar'),
                                    html.Div([], className = 'fill success_cercle', id = 'sale_cercle_fill'),
                                ], className = 'slice')
                            ], className = 'c100 p81 petit', id = 'sale_cercle')
                        ], className='progress')
                    ], className='middle'),
                    html.Small([], className='text-muted', id = 'sale_yesterday'),
                ], className='sales'),
                # -------------- END OF SALES -------------- #
                html.Div([
                    html.Span('bar_chart', className="material-icons-sharp span-icon"),
                    html.Div([
                        html.Div([
                            html.H3('Expances'),
                            html.H2([''], id = 'budget')
                        ], className='left'),
                        html.Div([
                            html.Div([
                                html.Span('', className='success', id = 'budget_percentage'), 
                                html.Div([
                                    html.Div([], className = 'bar success_cercle', id = 'budget_cercle_bar'),
                                    html.Div([], className = 'fill success_cercle', id = 'budget_cercle_fill'),
                                ], className = 'slice')
                            ], className = 'c100 p62 petit', id = 'budget_cercle')
                        ], className='progress')
                    ], className='middle'),
                    html.Small([], className='text-muted', id = 'budget_yesterday'),
                ], className='expances'),
                # -------------- END OF EXPANCES -------------- #
                html.Div([
                    html.Span('stacked_line_chart', className="material-icons-sharp span-icon"),
                    html.Div([
                        html.Div([
                            html.H3('Incomes'),
                            html.H2([''], id = 'income')
                        ], className='left'),
                        html.Div([
                            html.Div([
                                html.Span('', className='success', id = 'income_percentage'), 
                                html.Div([
                                    html.Div([], className = 'bar', id = 'income_cercle_bar'),
                                    html.Div([], className = 'fill', id ='income_cercle_fill'),
                                ], className = 'slice')
                            ], className = 'c100 p14 petit', id = 'income_cercle')
                        ], className='progress')
                    ], className='middle'),
                    html.Small([], className='text-muted', id = 'income_yesterday'),
                ], className='income'),
                # -------------- END OF INCOMES -------------- #
                html.Div([
                    html.Span('inventory_2', className="material-icons-sharp span-icon"),
                    html.Div([
                        html.Div([
                            html.H3('Products'),
                            html.H2('', id = 'nproducts')
                        ], className='left'),
                        html.Div([
                            html.Div([
                                html.Span('', className='success', id = 'nproducts_percentage'), 
                                html.Div([
                                    html.Div([], className = 'bar success_cercle', id = 'nproducts_cercle_bar'),
                                    html.Div([], className = 'fill success_cercle', id = 'nproducts_cercle_fill'),
                                ], className = 'slice')
                            ], className = 'c100 p35 petit', id = 'nproducts_cercle')
                        ], className='progress')
                    ], className='middle'),
                    html.Small([], className='text-muted', id = 'nproducts_yesterday'),
                ], className='sales')
            ], className='insights'),
            # --------------------- END OF INSIGHTS ------------------#

            html.Div([
                html.H1('SUMMARY'),
                html.Div([dcc.Graph(figure = go.Figure(), id = 'graph_dashboard')],  className='chart'),
                html.Div([dcc.Graph(figure = go.Figure(),id = 'graph_dashboard4')],  className='chart'),
                html.Div([dcc.Graph(figure = go.Figure(),id = 'graph_dashboard1')], className='chart'),
                html.Div([dcc.Graph(figure = go.Figure(),id = 'graph_dashboard2')], className='chart'),
                html.Div([dcc.Graph(figure = go.Figure(),id = 'graph_dashboard3')], className='chart'),
                html.Div([dcc.Graph(figure = go.Figure(),id = 'graph_dashboard5')], className='chart'),
                html.Div([dcc.Graph(figure = go.Figure(),id = 'graph_dashboard6')], className='chart'),
                html.Div([dcc.Graph(figure = go.Figure(),id = 'graph_dashboard7')], className='chart'),
            ], className = 'recent-orders')

        ]),
        # --------------- END OF MAIN ---------------------#
        html.Div([ 
            html.Div([
                dcc.RadioItems(
                    id = 'methode',
                    options=[
                        {'label': 'Par An', 'value': 'Par An'},
                        {'label': 'Par Mois', 'value': 'Par Mois'},
                        {'label': 'Par Jour', 'value': 'Par Jour'},
                    ],
                    value='Par Jour'
                ),
            ], className='show_methode'),
            html.Div(children = [], className='sales-analytics', id = 'sales-analytics')


        ], className='right')




    ], className='container')
]