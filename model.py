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
from datetime import datetime
from datetime import timedelta
from plotly.subplots import make_subplots
import sys


pathinfo = 'info_product.csv'
info_data = pd.read_csv(pathinfo, encoding='latin-1')


info_data['code_google'] = info_data['code_google'].astype(str)
dict_produit = dict(info_data[['code_google', 'product_name']].values)
dict_page = dict(info_data[['page', 'product_name']].values)
dict_product = dict(info_data[['produit', 'product_name']].values)
dict_cout = dict(info_data[['product_name', 'cout']].values)
dict_collection = dict(info_data[['product_name', 'collection']].values)


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

def change_result(x):
    if x >= 0 :
        return 'Positive'
    else : 
        return 'Negative'


# ========================================== DAshboard Functions ========================================

def define_graphs(df, col) :

    df = df[df['produit_Cible'] != '*']

    fig = px.bar(df[df['Result'] != 0], x="produit_Cible", y="Result", color = "produit_Cible",
                title ='Results Per Product', color_discrete_sequence=color)

    fig1 = px.bar(df[df['Link_Click'] > 0], x="produit_Cible", y="Link_Click", color = "produit_Cible", text='Link_Click',
                title ='Link_Click Per Product', color_discrete_sequence=color)


    dt = pd.DataFrame(df.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] != 'None']
    dt['Pourcentage'] = np.round(dt['Amout_Spent']*100/sum(dt['Amout_Spent']), 2)
    dt.loc[dt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dt = pd.DataFrame(dt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    dt1 = dt.copy()

    dt = pd.DataFrame(df.groupby('produit_Cible')['CA'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] != 'None']
    dt['Pourcentage'] = np.round(dt['CA']*100/sum(dt['CA']), 2)
    dt.loc[dt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dt = pd.DataFrame(dt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()

    fig2 = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "domain"}, {"type": "domain"}]],
        subplot_titles=("Percentage Of Budget For Each Product","Percentage Of Sales For Each Product")
    )


    fig2.add_trace(go.Pie(values = dt['Pourcentage'], labels = dt['produit_Cible'], hole=.5, marker_colors=color*len(dt) ),
                row=1, col=1)

    fig2.add_trace(go.Pie(values = dt1['Pourcentage'], labels = dt1['produit_Cible'], hole=.5, marker_colors=color*len(dt)  ),
                row=1, col=2)



    dt = pd.DataFrame(df.groupby('produit_Cible')['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] != 'None']
    dt['CPC'] = np.round(dt['Amout_Spent']/dt['Link_Click'], 2)

    fig3 = px.bar(dt[dt['CPC'] > 0], x="produit_Cible", y="CPC", color = "produit_Cible", text='CPC',title ='CPC Par Produit', color_discrete_sequence=color)

    
    dt = df.groupby('produit_Cible')['CA', 'Result'].sum()
    dt = dt.reset_index(level=0)
    dt = dt[dt['produit_Cible'] != 'None']
    dt['Taux_Result'] = dt['Result']*100/dt['CA']
    dt = dt.fillna(0)
    fig4 = px.bar(dt, x = 'produit_Cible', y = 'Taux_Result', color = 'produit_Cible', color_discrete_sequence=color, title = 'Income ROAS Per Product')

    dt = df.groupby('produit_Cible')['Count'].sum()
    dt = dt.reset_index(level=0)
    dt = dt[dt['produit_Cible'] != 'None']
    dt = dt.fillna(0)
    dt = dt[dt['Count'] != 0]
    fig5 = px.bar(dt, x = 'produit_Cible', y = 'Count', color = 'produit_Cible', color_discrete_sequence=color,  title = 'Sale Per Product')

    dt = df.groupby('produit_Cible')['Link_Click', 'Sales'].sum()
    dt = dt.reset_index(level=0)
    dt = dt[dt['produit_Cible'] != 'None']
    dt = dt.fillna(0)
    dt = dt[dt['Link_Click'] != 0]
    dt['Taux_cv'] = (dt['Sales']/dt['Link_Click']) * 100
    fig6 = px.bar(dt, x = 'produit_Cible', y = 'Taux_cv', color = 'produit_Cible', color_discrete_sequence=color,  title = 'Convertion Rate Per Product')

    dt = df.groupby('produit_Cible')['Amout_Spent', 'Count'].sum()
    dt = dt.reset_index(level=0)
    dt = dt[dt['produit_Cible'] != 'None']
    dt = dt.fillna(0)
    dt = dt[dt['Count'] != 0]
    dt['Cost_Sale'] = dt['Amout_Spent']/dt['Count']
    fig7 = px.bar(dt, x = 'produit_Cible', y = 'Cost_Sale', color = 'produit_Cible', color_discrete_sequence=color,  title = 'Cost For Sale Per Product')


    fig.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig1.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig2.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig3.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig4.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig5.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig6.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig7.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    return fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7


def data_today_yesterday(df, text):

    df['Date '] = pd.to_datetime(df['Date '])

    if text == 'Par Jour' :
        tdy = list(df['Date '].unique())[-1]
        yesterdy = list(df['Date '].unique())[-2]
        return str(tdy)[:10], df[df['Date '] == tdy], df[df['Date '] == yesterdy], 'Date '

    elif text == 'Par Mois' :
        df['date_month'] = df['Date '].dt.to_period('M')
        data_month = df.groupby(['date_month', 'Platforme', 'produit_Cible'])['Amout_Spent', 'Count', 'Link_Click', 'CA', 'Result', 'Sales'].sum()
        data_month = data_month.reset_index()
        tdy = list(df['date_month'].unique())[-1]
        yesterdy = list(df['date_month'].unique())[-2]

        return str(pd.to_datetime(str(tdy)))[:7], data_month[data_month['date_month'] == tdy], data_month[data_month['date_month'] == yesterdy], 'date_month'
    elif text == 'Par An' :  
        df['date_year'] = df['Date '].dt.to_period('Y')
        data_year = df.groupby(['date_year', 'Platforme', 'produit_Cible'])['Amout_Spent', 'Count', 'Link_Click', 'CA', 'Result', 'Sales'].sum()
        data_year = data_year.reset_index()
        tdy = list(df['date_year'].unique())[-1]
        if len(list(df['date_year'].unique())) == 1 : 
            yesterdy = '2021'
        else :
            yesterdy = list(df['date_year'].unique())[-2]

        return str(tdy), data_year[data_year['date_year'] == tdy], data_year[data_year['date_year'] == yesterdy], 'date_year'

def division(x, y) :
    if y == 0 :
        return [100, ' %']
    else : 
        return [np.round(((x/y)-1)*100, 2), ' %']




def creates_set_graph(df) : 
    Date = []

    df['Date '] = pd.to_datetime(df['Date '])

    dt = df.groupby('Date ')["Amout_Spent", "CA", "Cout", "Result"].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] != 'None']
    dt['Pourcentage'] = np.round(dt['Amout_Spent']*100/sum(dt['Amout_Spent']), 2)
    dt.loc[dt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dt = pd.DataFrame(dt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    Date.append(dt)

    df1 = pd.DataFrame(df.groupby(['Date '])['Amout_Spent'].sum()).reset_index()
    df2 = pd.DataFrame(df.groupby(['Date ', 'produit_Cible'])['Amout_Spent'].sum()).reset_index()
    dt = df1.merge(df2, on = 'Date ', how = 'outer')
    dt['Pourcentage'] = np.round(dt['Amout_Spent_y']*100/dt['Amout_Spent_x'], 2)
    dt['Pourcentage'] = dt['Pourcentage'].fillna(0)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('produit_Cible')['CA'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] != 'None']
    dt['Pourcentage'] = np.round(dt['CA']*100/sum(dt['CA']), 2)
    dt.loc[dt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dt = pd.DataFrame(dt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    Date.append(dt)

    df1 = pd.DataFrame(df.groupby(['Date '])['CA'].sum()).reset_index()
    df2 = pd.DataFrame(df.groupby(['Date ', 'produit_Cible'])['CA'].sum()).reset_index()
    dt = df1.merge(df2, on = 'Date ', how = 'outer')
    dt['Pourcentage'] = np.round(dt['CA_y']*100/dt['CA_x'], 2)
    dt['Pourcentage'] = dt['Pourcentage'].fillna(0)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('produit_Cible')['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] != 'None']
    dt['CPC'] = np.round(dt['Amout_Spent']/dt['Link_Click'], 2)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('Date ')['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dt['CPC'] = np.round(dt['Amout_Spent']/dt['Link_Click'], 2)
    dt['CPC'] = dt['CPC'].fillna(0)
    Date.append(dt)


    ctr = df[['Date ', 'Link_Click', 'CTR', 'produit_Cible']]
    ctr['Vue'] = ctr['Link_Click']/(ctr['CTR']/100)
    ctr.loc[ctr.Vue.isnull(), 'Vue'] = 0
    df1 = ctr.groupby('produit_Cible')['Link_Click', 'Vue'].mean()
    df1 = df1.reset_index(level=0)
    if 'None' in df1['produit_Cible'].unique() :
        df1 = df1[df1['produit_Cible'] != 'None']
    df1['CTR'] = df1['Link_Click']*100/df1['Vue']
    df1['CTR']=df1['CTR'].apply(lambda x:round(x,2))
    df1['Link_Click']=df1['Link_Click'].apply(lambda x:round(x,2))
    Date.append(df1)

    dt = df.groupby('Date ')["Link_Click"].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    link = df[['Date ', 'Link_Click', 'produit_Cible', 'CTR']]
    link['Impressions'] = link['Link_Click']/link['CTR']
    link.loc[link.Impressions.isnull(), 'Impressions'] = 0
    dt = link.groupby('Date ')["Link_Click", "Impressions"].sum()
    dt = dt.reset_index(level=0)
    dt['CTR'] = dt['Link_Click']/dt['Impressions']
    dt.loc[dt.CTR.isnull(), 'CTR'] = 0
    Date.append(dt)

    dt = df.groupby('produit_Cible')['CA', 'Result'].sum()
    dt = dt.reset_index(level=0)
    dt = dt[dt['produit_Cible'] != 'None']
    dt['Taux_Result'] = dt['Result']*100/dt['CA']
    dt = dt.fillna(0)
    Date.append(dt)

    dt = df.groupby('Date ')['Link_Click', "Panier", "Check_Out", 'Sales'].sum()
    dt = dt.reset_index(level=0)
    dt['Tx_Conv'] = np.round(dt['Sales']*100/dt['Link_Click'], 2)
    dt['Tx_Panier'] = np.round(dt['Panier']*100/dt['Link_Click'], 2)
    dt['Tx_Check_Out'] = np.round(dt['Check_Out']*100/dt['Link_Click'], 2)
    dt = dt.fillna(0)
    Date.append(dt)

    

    dt = df.groupby('produit_Cible')['Count'].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    dt = df.groupby('produit_Cible')["Amout_Spent", 'Link_Click','Count'].sum()
    dt = dt.reset_index(level=0)
    dt['click_for_sale'] = dt['Link_Click']/dt['Count']
    dt['Cost_for_Sale'] = dt['Amout_Spent']/dt['Count']
    dt = dt.fillna(0)
    Date.append(dt)

    dt = df[~df['produit_Cible'].isin(['None', '*'])]
    dt['Result_Cat'] = dt['Result']
    dt['Result_Cat'] = dt['Result_Cat'].apply(lambda x : change_result(x))
    dt1 = pd.DataFrame(dt[dt['Result_Cat'] == 'Positive'].groupby(['produit_Cible'])['Result_Cat'].count()).reset_index()
    dt2 = pd.DataFrame(dt[dt['Result_Cat'] == 'Negative'].groupby(['produit_Cible'])['Result_Cat'].count()).reset_index()
    dt = dt1.merge(dt2, on = 'produit_Cible')
    dt = dt.fillna(0)
    dt['Pourcentage_Positive'] = np.round(dt['Result_Cat_x']*100/(dt['Result_Cat_x']+dt['Result_Cat_y']), 2)
    dt = dt.fillna(0)
    dt['Pourcentage_Negative'] = 100 - dt['Pourcentage_Positive']
    Date.append(dt)

    dt = df.groupby('Date ')['Count'].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    return Date

def results_dashboard(products, df, df1) : 
    children = [html.H1('Results')]
    for p in products :
        if p in df['produit_Cible'].unique() :
            dt = df[df['produit_Cible'] == p]
            dt1 = df1[df1['produit_Cible'] == p]
            if len(dt1) == 0 :
                dt1 = dt.copy()
                for col in dt1.columns:
                    dt1[col].values[:] = 0
            children.append(html.Div([
                        html.Img(src = '/assets/products/' + p + '.png'),
                        html.H4(p),
                        html.Div([
                            html.H5('Budget'),
                            html.H3([np.round(sum(dt['Amout_Spent']),2), ' €']),
                            html.Small(children = division(sum(dt['Amout_Spent']), sum(dt1['Amout_Spent'])), 
                        style = {'color' : 'rgb(255, 67, 54)'} if division(sum(dt['Amout_Spent']), sum(dt1['Amout_Spent']))[0] < 0 else {'color' : 'rgb(34, 202, 75)'}), 
                        ], className = 'bonds'),
                        html.Div([
                            html.H5('CA'),
                            html.H3([np.round(sum(dt['CA']),2), ' €']),
                            html.Small(children = division(sum(dt['CA']), sum(dt1['CA'])), 
                        style = {'color' : 'rgb(255, 67, 54)'} if division(sum(dt['CA']), sum(dt1['CA']))[0] < 0 else {'color' : 'rgb(34, 202, 75)'}), 
                        ], className = 'amount')
                    ], className='item') )
    return children


# ============================= ANALYTICS PAGE =====================================

def best_produit_analysis(dt, dt1) : 

    dt2 = pd.DataFrame(dt.groupby('produit_Cible')['Result'].sum()).reset_index()

    top_products = dt2.sort_values(by='Result', ascending=False).head(3)

    top_product_names = top_products['produit_Cible'].tolist()

    children = [html.H1("Best 3 Products", style = {'marginTop' : '1rem', 'marginLeft' : '1rem'})]

    for name in top_product_names : 

        sale_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'CA']), sum(dt1.loc[dt1['produit_Cible'] == name, 'CA']))
        result_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Result']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Result']))
        
        try : 
            cpc = np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent'])/sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click']),2)
        except : 
            cpc = 0
        try : 
            cpc_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click'])/sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Link_Click'])/sum(dt1.loc[dt1['produit_Cible'] == name, 'Amout_Spent']))
        except : 
            cpc_percentage = [100, '%']

        try : 
            cost_sale = np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent'])/sum(dt.loc[dt['produit_Cible'] == name, 'Count']),2)
        except : 
            cost_sale = 0   
        try :    
            cost_sale_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent'])/sum(dt.loc[dt['produit_Cible'] == name, 'Count']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Amout_Spent'])/sum(dt1.loc[dt1['produit_Cible'] == name, 'Count']))
        except : 
            cost_sale_percentage = [100, '%']

        try : 
            conv_rate = np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Sales'])/sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click']) * 100, 2)
        except : 
            conv_rate = 0
        try :
            conv_rate_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Sales'])/sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Sales'])/sum(dt1.loc[dt1['produit_Cible'] == name, 'Link_Click']))
        except : 
            conv_rate_percentage = [100, '%']


        children.append(dbc.Col([
                                html.Div([
                                    html.Img(src="/assets/products/" + name + ".png"),
                                ], className = 'attribut_img'), # Image du produit
                                html.Div([
                                    html.H2(name), # Nom du produit
                                    html.Div([
                                        html.H3("Sale"),
                                        html.H3([np.round(sum(dt.loc[dt['produit_Cible'] == name, 'CA']), 2), ' €']),
                                        html.H3(sale_percentage, style = {'color' : 'rgb(255, 67, 54)'} if sale_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Income"),
                                        html.H3([np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Result']), 2), ' €']),
                                        html.H3(result_percentage, style = {'color' : 'rgb(255, 67, 54)'} if result_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Cost per click"),
                                        html.H3([cpc,  ' €']),
                                        html.H3(cpc_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cpc_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Cost per sale"),
                                        html.H3([cost_sale,  ' €']),
                                        html.H3(cost_sale_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cost_sale_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Convertion rate"),
                                        html.H3([conv_rate,  '%']),
                                        html.H3(conv_rate_percentage, style = {'color' : 'rgb(255, 67, 54)'} if conv_rate_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                ]),
                            ], width=4))
        
    return children 




def define_class(n) : 
    if n >= 0 : 
        return 'success'
    else : 
        return 'danger'


def define_graphs_analysis(df) : 
    
    dt = creates_set_graph(df)
    
    #graph1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dt[0]['Date '], y=dt[0]["Amout_Spent"],
                        mode='lines',
                        name = 'Budget',
                        marker_color=color_red[0]))
    fig.add_trace(go.Scatter(x=dt[0]['Date '], y=dt[0]["CA"],
                        mode='lines',
                        name = "Sales",
                        marker_color=color[1]))
    fig.add_trace(go.Scatter(x=dt[0]['Date '], y=dt[0]["Result"],
                        mode='lines',
                        name = "Income",
                        marker_color=color[0]))
    fig.update_layout(
        title="Evolution Of Sales, Budget And Income",
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph2
    fig2 = px.bar(dt[10][dt[10]['Result'] != 0], x = 'produit_Cible', y = 'Result', color = 'produit_Cible', color_discrete_sequence=color, title = 'Income Per Product') 
    fig2.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph3
    fig3 = px.bar(dt[12][dt[12]['Count'] > 0], x = 'produit_Cible', y = 'Count', color = 'produit_Cible', color_discrete_sequence=color, title = 'Sale Per Product')
    fig3.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph4
    fig4 = px.bar(dt[13][dt[13]['click_for_sale'] > 0], x = 'produit_Cible', y = 'click_for_sale', color = 'produit_Cible', color_discrete_sequence=color, title = 'Visit For One Sale')
    fig4.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph5
    fig5 = px.bar(dt[13][dt[13]['Cost_for_Sale'] > 0], x = 'produit_Cible', y = 'Cost_for_Sale', color = 'produit_Cible', color_discrete_sequence=color, title = 'Cost For One Sale')
    fig5.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph6
    fig6 = px.pie(dt[1], values='Pourcentage', names='produit_Cible', title='Percentage Of Budget For Each Product', 
             color_discrete_sequence=color, hole=.5)
    fig6.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph7
    fig7 = px.pie(dt[3], values='Pourcentage', names='produit_Cible', title='Percentage Of Sales For Each Product', 
             color_discrete_sequence=color, hole=.5)
    fig7.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph8
    fig8 = px.bar(dt[5][dt[5]['CPC'] > 0], x="produit_Cible", y="CPC", color = "produit_Cible", text='CPC',color_discrete_sequence=color,
             title ='CPC Per Product')
    fig8.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph9
    fig9 = px.area(dt[8], x="Date ", y="Link_Click", title="Visits Evolution", color_discrete_sequence=[color[1]])
    fig9.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )    

    #graph 10
    fig10 = px.bar(dt[7][dt[7]['Link_Click'] > 0], x="produit_Cible", y="Link_Click", color = "produit_Cible", text='Link_Click',color_discrete_sequence=color,
                title ="Average Visit Per Product")   
    fig10.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )   

    fig11 = px.area(dt[6], x="Date ", y="CPC", title="CPC Evolution", color_discrete_sequence=color)
    fig11.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph12
    fig12 = go.Figure()
    fig12.add_trace(go.Scatter(x=dt[11]['Date '], y=dt[11]["Tx_Panier"],
                        mode='lines',
                        name = 'Shopping Cart Rate',
                        marker_color=color[7]))
    fig12.add_trace(go.Scatter(x=dt[11]['Date '], y=dt[11]["Tx_Check_Out"],
                        mode='lines',
                        name = "Check Out Rate",
                        marker_color=color[1]))
    fig12.add_trace(go.Scatter(x=dt[11]['Date '], y=dt[11]["Tx_Conv"],
                        mode='lines',
                        name = "Order Rate",
                        marker_color=color[0]))
    fig12.update_layout(
        title="Shopping Cart Rate, Check Out Rate and Order Rate Evolution",
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph13
    fig13 = px.area(dt[4], x="Date ", y="Pourcentage", title="Sales Percentage Evolution Of Each Product", 
              color = 'produit_Cible', color_discrete_sequence=color)
    fig13.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph14
    fig14 = px.area(dt[2], x="Date ", y="Pourcentage", title="Budget Percentage Evolution Of Each Product", 
              color = 'produit_Cible', color_discrete_sequence=color)
    fig14.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    return fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13, fig14





# ============================= PRODUCTS PAGE =====================================


def define_graphs_products(df) : 
    
    dt = creates_set_graph(df)
    
    #graph1
    fig = px.area(dt[0], x="Date ", y="CA", title="Sales Evolution", color_discrete_sequence=[color[1]])
    fig.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        height = 380,
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph2
    fig2 = px.area(dt[0], x="Date ", y="Result", title="Income Evolution", color_discrete_sequence=[color[1]]) 
    fig2.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        height = 380,
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )


    #graph3
    fig3 = px.area(dt[8], x="Date ", y="Link_Click", title="Visits Evolution", color_discrete_sequence=[color[1]])
    fig3.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        height = 380,
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )    

      
    #graph4
    fig4 = px.area(dt[6], x="Date ", y="CPC", title="CPC Evolution", color_discrete_sequence=color)
    fig4.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph 5
    try : 
        pourcentage = list(dt[14][['Pourcentage_Positive', 'Pourcentage_Negative']].values[0])
    except : 
        pourcentage = [100, 0]
    fig5 = px.pie(values=pourcentage, names=['Win', 'Loss'], title="Product's Result", 
             color_discrete_sequence=color, hole = .7)

    fig5.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph6
    fig6 = px.area(dt[15], x="Date ", y="Count", title="Product Sale Unit Evolution", color_discrete_sequence=color)
    fig6.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    return fig, fig2, fig3, fig4, fig5, fig6


def attribut_products_var(df, df1):

    try : 
        visit_for_sale_tdy = np.round(sum(df['Link_Click'])/sum(df['Count']), 2)
    except : 
        visit_for_sale_tdy = 0
    try : 
        visit_forsale_percentage = division(visit_for_sale_tdy, np.round(sum(df1['Link_Click'])/sum(df1['Count']), 2))
    except : 
        visit_forsale_percentage = [100, '%']

    try :
        cost_for_sale_tdy = np.round(sum(df['Amout_Spent'])/sum(df['Count']), 2)
    except : 
        cost_for_sale_tdy = 0
    try :
        cost_percentage = division(cost_for_sale_tdy, np.round(sum(df1['Amout_Spent'])/sum(df1['Count']), 2))
    except :
        cost_percentage = [100, '%'] 

    try : 
        roas_in = np.round(sum(df['Result'])*100/sum(df['CA']), 2)
    except : 
        roas_in = 0
    try :
        roas_percentage = division(roas_in, np.round(sum(df1['Result'])*100/sum(df1['CA']), 2))
    except : 
        roas_percentage = [100, '%']

    highest = np.round(max(df['CA']),2)
    try :
        highest_percentage = division(highest, np.round(max(df1['CA']),2))
    except : 
        highest_percentage = [100, '%']

    visit = np.round(sum(df['Link_Click']), 2)
    try : 
        visit_percentage = division(visit, np.round(sum(df1['Link_Click']), 2))
    except : 
        visit_percentage = [100, '%']

    try : 
        cpc = np.round(sum(df['Amout_Spent'])/visit, 2)
    except : 
        cpc = 0
    try :
        cpc_percentage = division(cpc, np.round(sum(df['Amout_Spent'])/sum(df1['Link_Click']), 2))
    except : 
        cpc_percentage = [100, '%']

    df['Impres'] = np.round(df['Link_Click']*100/df['CTR'])
    df = df.fillna(0)
    
    ctr = np.round(sum(df['Link_Click'])*100/sum(df['Impres']), 2) if sum(df['Impres']) != 0 else 0
    try : 
        df1['Impres'] = np.round(df1['Link_Click']*100/df1['CTR'])
        df1 = df1.fillna(0)
        ctr_percentage = division(ctr, np.round(sum(df1['Link_Click'])*100/sum(df1['Impres']), 2))
    except : 
        ctr_percentage = [100, '%']

    try : 
        cv_rate = np.round(sum(df['Sales'])*100/sum(df['Link_Click']), 2)
    except : 
        cv_rate = 0
    try :
        cv_rate_percentage = division(cv_rate, np.round(sum(df1['Sales'])*100/sum(df1['Link_Click']), 2))
    except : 
        cv_rate_percentage = [100, '%']

    return visit_for_sale_tdy, visit_forsale_percentage, cost_for_sale_tdy, cost_percentage, roas_in, roas_percentage, highest, highest_percentage, visit, visit_percentage, cpc, cpc_percentage, ctr, ctr_percentage, cv_rate, cv_rate_percentage


def change_date(df, start, end) :

    df1 = df.copy()

    if start is not None and end is not None:
        df = df.loc[(start <= df['Date ']) & (df['Date '] <= end)]
        n_days = len(df['Date '].unique())
        end = start
        start = str(datetime.strptime(start, "%Y-%m-%d") -  timedelta(days=n_days))[:10]
        df1 = df1.loc[(start <= df1['Date ']) & (df1['Date '] <= end)]
    else :
        df1 = pd.DataFrame(columns=df.columns)

    if len(df1) == 0 :
        df1 = df.copy()
        for col in df1.columns:
            df1[col].values[:] = 0

    return df, df1





def attribut_products_consts(df, df1, value):

    dt = pd.DataFrame(df.groupby('produit_Cible')['CA'].sum()).reset_index()
    total_CA = sum(dt['CA'])
    dt['Pourcentage'] = np.where(total_CA != 0, np.round(dt['CA']*100/total_CA, 2), 0)

    dt = pd.DataFrame(dt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] == value]
    sale_pr = dt['Pourcentage'].item()
    
    try : 
        dt1 = pd.DataFrame(df1.groupby('produit_Cible')['CA'].sum()).reset_index()
        total_CA = sum(dt1['CA'])
        dt1['Pourcentage'] = np.where(total_CA != 0, np.round(dt1['CA']*100/total_CA, 2), 0)

        dt1 = pd.DataFrame(dt1.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
        dt1 = dt1[dt1['produit_Cible'] == value]
        sale_pr_percentage = division(sale_pr, dt1['Pourcentage'].item())
    except : 
        sale_pr_percentage = [100, '%']

    
    dt = pd.DataFrame(df.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
    total_budget = sum(dt['Amout_Spent'])
    dt['Pourcentage'] = np.where(total_budget != 0, np.round(dt['Amout_Spent']*100/sum(dt['Amout_Spent']), 2), 0)

    dt = pd.DataFrame(dt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    dt = dt[dt['produit_Cible'] == value]
    budget_pr = dt['Pourcentage'].item()
    
    try : 
        dt1 = pd.DataFrame(df1.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
        total_budget = sum(dt1['Amout_Spent'])
        dt1['Pourcentage'] = np.where(total_budget != 0, np.round(dt1['Amout_Spent']*100/total_budget, 2), 0)
        dt1 = pd.DataFrame(dt1.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
        dt1 = dt1[dt1['produit_Cible'] == value]
        budget_pr_percentage = division(sale_pr, dt1['Pourcentage'].item())
    except : 
        budget_pr_percentage = [100, '%']

    return sale_pr, sale_pr_percentage, budget_pr, budget_pr_percentage



def attribut_products_week(df, value) :

    dt = df.loc[df['produit_Cible'] == value]
    dt = dt[['Date ', 'CA']]
    
    max_7 = max(dt.iloc[-7:, 1])
    try : 
        max_7_percentage = division(max_7, max(dt.iloc[-8:-1, 1]))
    except : 
        max_7_percentage = [100, '%']

    max_30 = max(dt.iloc[-30:, 1])
    try : 
        max_30_percentage = division(max_30, max(dt.iloc[-31:-1, 1]))
    except : 
        max_30_percentage = [100, '%']

    max_52 = max(dt.iloc[-7*52:, 1])
    try : 
        max_52_percentage = division(max_52, max(dt.iloc[(-52*7)-1 :-1, 1]))
    except : 
        max_52_percentage = [100, '%']


    return max_7, max_7_percentage, max_30, max_30_percentage, max_52, max_52_percentage



def attribut_products(df, value, start, end) : 

    max_7, max_7_percentage, max_30, max_30_percentage, max_52, max_52_percentage = attribut_products_week(df, value)

    dt, dt1 = change_date(df, start, end)

    sale_pr, sale_pr_percentage, budget_pr, budget_pr_percentage = attribut_products_consts(dt, dt1, value)

    dt = dt.loc[dt['produit_Cible'] == value]

    visit_for_sale_tdy, visit_forsale_percentage, cost_for_sale_tdy, cost_percentage, roas_in, roas_percentage, highest, highest_percentage, visit, visit_percentage, cpc, cpc_percentage, ctr, ctr_percentage, cv_rate, cv_rate_percentage = attribut_products_var(dt, dt1)
    
    children = [html.Div([
                    html.Div([
                        html.Img(src = '/assets/products/' + value +'.png'),
                    ], className = 'attribut_img'),
                    html.Br(),
                    html.Div([
                        html.H3('Visit For Sale'),
                        html.H3(visit_for_sale_tdy), 
                        html.H3(visit_forsale_percentage, style = {'color' : 'rgb(255, 67, 54)'} if visit_forsale_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Cost For Sale'),
                        html.H3([cost_for_sale_tdy, ' €']), 
                        html.H3(cost_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cost_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('% Sales'),
                        html.H3([sale_pr, '%']), 
                        html.H3(sale_pr_percentage, style = {'color' : 'rgb(255, 67, 54)'} if sale_pr_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('% Budget'),
                        html.H3([budget_pr, '%']), 
                        html.H3(budget_pr_percentage, style = {'color' : 'rgb(255, 67, 54)'} if budget_pr_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Income/Sale'),
                        html.H3([roas_in, '%']), 
                        html.H4(roas_percentage, style = {'color' : 'rgb(255, 67, 54)'} if roas_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Highest Sale'),
                        html.H3([highest, ' €']), 
                        html.H3(highest_percentage, style = {'color' : 'rgb(255, 67, 54)'} if roas_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Week High/Low'),
                        html.H3([max_7, ' €']), 
                        html.H3(max_7_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if max_7_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Month High/Low'),
                        html.H3([max_30, ' €']), 
                        html.H3(max_30_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if max_30_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('52 Week High/Low'),
                        html.H3([max_52, ' €']), 
                        html.H3(max_52_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if max_52_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Visitors'),
                        html.H3(visit), 
                        html.H3(visit_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if visit_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('CPC'),
                        html.H3([cpc, ' €']), 
                        html.H3(cpc_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cpc_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('CTR'),
                        html.H3([ctr, '%']), 
                        html.H3(ctr_percentage, style = {'color' : 'rgb(255, 67, 54)'} if ctr_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Conversion Rate'),
                        html.H3([cv_rate, '%']), 
                        html.H3(cv_rate_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cv_rate_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                ], className = 'attributs')]

    return children



# =============================== UpDate Page =================================

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename :
            if 'sales' in filename : 
                df = pd.read_csv(io.StringIO(decoded.decode('latin-1')))
            else : 
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df
        elif 'xls' in filename :
            df = pd.read_excel(io.BytesIO(decoded))
            return df
        elif 'xlsx' in filename :
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return print(e)


def parse_contents1(contents, filename):
    content_type, content_string = contents.split(',')
    
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename :
            df = pd.read_csv(io.StringIO(decoded.decode('latin-1')))
            return df
        elif 'xls' in filename :
            df = pd.read_excel(io.BytesIO(decoded))
            return df
        elif 'xlsx' in filename :
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return print(e)


def proccess_item_id(x, dict_p) : 
    if x[11:24] + "'" in dict_p.keys() :
        return dict_p[x[11:24] + "'"]
    else : 
        return "*"

def float_x(x):
    return float('.'.join(x.split(',')))

def impression(x) :
    l = []
    nbr = ['0','1','2','3','4','5','6','7','8','9']
    for i in range(len(x)) :
        if x[i] in nbr :
            l.append(x[i])
    n = ''.join(l)
    return int(n)



def compagne_google(google, filename, info_pro) : 
    columns = list(info_pro.columns)
    dict_produit = dict(info_pro[[columns[2], columns[1]]].values)

    date = filename[7:-5]
    date = date.replace('_', '-')


    google['Item ID'] = google['Item ID'].apply(lambda x : proccess_item_id(x, dict_produit) )

    google_group_cost = pd.DataFrame(google.groupby('Item ID')['Cost'].sum()).reset_index()

    google['Impr.'] = google['Impr.'].apply(lambda x : int(x.replace(",", "")))

    google_gr_click = pd.DataFrame(google.groupby('Item ID')['Clicks', 'Impr.'].sum()).reset_index()
    google_gr_click['CTR'] = np.round(google_gr_click['Clicks']*100/google_gr_click['Impr.'], 2)

    google_final = google_gr_click.merge(google_group_cost, on = ['Item ID'], how = 'outer')
    google_final['Platforme'] = 'Google'
    google_final['Date '] = date
    google_final['Date '] = pd.to_datetime(google_final['Date '])
    google_final['Date '] = google_final['Date '].dt.strftime('%m/%d/%Y')
    google_final['Date '] = pd.to_datetime(google_final['Date '])

    google_final = google_final.rename(columns = {'Item ID' : 'produit_Cible', 'Cost' : 'Amout_Spent', 'Clicks' : 'Link_Click'})
    google_final = google_final[['Date ', 'Platforme','Amout_Spent', 'produit_Cible', 'Link_Click', 'CTR']]


    return google_final



def change_page(x, dict_p) :
    if x in dict_p.keys() :
        return dict_p[x]
    else :
        return '*'

def visite(data, filename, info_pro) :

    columns = list(info_pro.columns)
    dict_page = dict(info_pro[[columns[0], columns[1]]].values)
    
    date = filename[:-4].split('_')[-1]

    data["page_path"] = data["page_path"].apply(lambda x : change_page(x, dict_page))
    data = data[data['page_path'] != '*']
    data['Date '] = date
    data = data[['Date ', 'page_path', 'total_carts', 'total_checkouts', 'total_orders_placed']]

    data = data.rename(columns={"page_path": 'produit_Cible', 'total_carts' : 'Panier', 'total_checkouts' : 'Check_Out',  
                               'total_orders_placed' : 'Sales'})

    data =data.sort_values(by=['produit_Cible'])

    data['Date '] = pd.to_datetime(data['Date '])
    data['Date '] = data['Date '].dt.strftime('%m/%d/%Y')
    data['Date '] = pd.to_datetime(data['Date '])
    
    return data

def change_product(x, dict_p) :
    if x in dict_p.keys() :
        return dict_p[x]
    else :
        return '*'

def change_prix(x, dict_p) :
    if x in dict_p.keys() :
        return dict_p[x]
    else :
        return '*'

def order(data, filename, info_pro) : 
    date = filename[:-4].split('_')[-1]

    columns = list(info_pro.columns)
    dict_product = dict(info_pro[[columns[3], columns[1]]].values)
    dict_cout = dict(info_pro[[columns[1], columns[4]]].values)

    data["product_title"] = data["product_title"].apply(lambda x : change_page(x, dict_product))
    
    data = data[data['product_title'] != '*']

    data['Date '] = date
    
    data = data[['Date ', 'product_title', 'net_quantity', 'net_sales', 'discounts']]
    
    data['Cout'] = data['product_title']
    data['Cout'] = data['Cout'].apply(lambda x : change_prix(x, dict_cout))
    data['Cout'] = (data['Cout']+1)*data['net_quantity'] 
    
    data = data.rename(columns={"product_title": 'produit_Cible', 'net_quantity' : 'Count', 'net_sales' : 'CA'})
    
    data = data[['Date ', 'produit_Cible', 'Count', 'CA', 'Cout']]

    data = data.sort_values(by=['produit_Cible'])

    data['Date '] = pd.to_datetime(data['Date '])
    data['Date '] = data['Date '].dt.strftime('%m/%d/%Y')
    data['Date '] = pd.to_datetime(data['Date '])
    
    return data


def joining_set(df1, df2, df3) :

    df = df1.merge(df2, on = ['Date ', 'produit_Cible'], how = 'outer')   
    df = df.merge(df3, on = ['Date ', 'produit_Cible'], how = 'outer')     

    df['Platforme'] = 'Google'

    df= df.fillna(0)

    df['Tx_Panier'] = np.round(df['Panier']*100/df['Link_Click'], 2)
    df['Tx_Check_Out'] = np.round(df['Check_Out']*100/df['Link_Click'],2)
    df['Tx_Conv'] = np.round(df['Sales']*100/df['Link_Click'],2)

    df = df.fillna(0)

    df['Result'] = df['CA'] - df['Cout'] - df['Amout_Spent']

    df['Name_produit'] = df['produit_Cible']
    df.loc[df['Count'] == 0, 'Name_produit'] = 'None'

    df = df[['Date ', 'Platforme', 'Amout_Spent', 'produit_Cible', 'Link_Click',
       'CTR', 'Panier','Tx_Panier', 'Check_Out','Tx_Check_Out', 'Sales','Tx_Conv','Name_produit',  'Count', 'CA', 'Cout','Result']]

    return df


def update_google(df1, df2, df3, filename1, filename2, filename3, info_pro) :
    df1 = compagne_google(df1, filename1, info_pro)
    df2 = visite(df2, filename2, info_pro)
    df3 = order(df3, filename3, info_pro)
    return joining_set(df1, df2, df3)



# ================== PAGE COLLECTION ===========================

def creates_set_graph_collection(df) : 
    Date = []

    df['Date '] = pd.to_datetime(df['Date '])

    dt = df.groupby('Date ')["Amout_Spent", "CA", "Cout", "Result"].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('collection')['Amout_Spent'].sum()).reset_index()
    dt = dt[dt['collection'] != 'None']
    dt['Pourcentage'] = np.round(dt['Amout_Spent']*100/sum(dt['Amout_Spent']), 2)
    dt.loc[dt['Pourcentage'] < 1, 'collection'] = 'others'
    dt = pd.DataFrame(dt.groupby('collection')['Pourcentage'].sum()).reset_index()
    Date.append(dt)

    df1 = pd.DataFrame(df.groupby(['Date '])['Amout_Spent'].sum()).reset_index()
    df2 = pd.DataFrame(df.groupby(['Date ', 'collection'])['Amout_Spent'].sum()).reset_index()
    dt = df1.merge(df2, on = 'Date ', how = 'outer')
    dt['Pourcentage'] = np.round(dt['Amout_Spent_y']*100/dt['Amout_Spent_x'], 2)
    dt['Pourcentage'] = dt['Pourcentage'].fillna(0)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('collection')['CA'].sum()).reset_index()
    dt = dt[dt['collection'] != 'None']
    dt['Pourcentage'] = np.round(dt['CA']*100/sum(dt['CA']), 2)
    dt.loc[dt['Pourcentage'] < 1, 'collection'] = 'others'
    dt = pd.DataFrame(dt.groupby('collection')['Pourcentage'].sum()).reset_index()
    Date.append(dt)

    df1 = pd.DataFrame(df.groupby(['Date '])['CA'].sum()).reset_index()
    df2 = pd.DataFrame(df.groupby(['Date ', 'collection'])['CA'].sum()).reset_index()
    dt = df1.merge(df2, on = 'Date ', how = 'outer')
    dt['Pourcentage'] = np.round(dt['CA_y']*100/dt['CA_x'], 2)
    dt['Pourcentage'] = dt['Pourcentage'].fillna(0)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('collection')['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dt = dt[dt['collection'] != 'None']
    dt['CPC'] = np.round(dt['Amout_Spent']/dt['Link_Click'], 2)
    Date.append(dt)

    dt = pd.DataFrame(df.groupby('Date ')['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dt['CPC'] = np.round(dt['Amout_Spent']/dt['Link_Click'], 2)
    dt['CPC'] = dt['CPC'].fillna(0)
    Date.append(dt)


    ctr = df[['Date ', 'Link_Click', 'CTR', 'collection']]
    ctr['Vue'] = ctr['Link_Click']/(ctr['CTR']/100)
    ctr.loc[ctr.Vue.isnull(), 'Vue'] = 0
    df1 = ctr.groupby('collection')['Link_Click', 'Vue'].mean()
    df1 = df1.reset_index(level=0)
    if 'None' in df1['collection'].unique() :
        df1 = df1[df1['collection'] != 'None']
    df1['CTR'] = df1['Link_Click']*100/df1['Vue']
    df1['CTR']=df1['CTR'].apply(lambda x:round(x,2))
    df1['Link_Click']=df1['Link_Click'].apply(lambda x:round(x,2))
    Date.append(df1)

    dt = df.groupby('Date ')["Link_Click"].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    link = df[['Date ', 'Link_Click', 'collection', 'CTR']]
    link['Impressions'] = link['Link_Click']/link['CTR']
    link.loc[link.Impressions.isnull(), 'Impressions'] = 0
    dt = link.groupby('Date ')["Link_Click", "Impressions"].sum()
    dt = dt.reset_index(level=0)
    dt['CTR'] = dt['Link_Click']/dt['Impressions']
    dt.loc[dt.CTR.isnull(), 'CTR'] = 0
    Date.append(dt)

    dt = df.groupby('collection')['CA', 'Result'].sum()
    dt = dt.reset_index(level=0)
    dt = dt[dt['collection'] != 'None']
    dt['Taux_Result'] = dt['Result']*100/dt['CA']
    dt = dt.fillna(0)
    Date.append(dt)

    dt = df.groupby('Date ')['Link_Click', "Panier", "Check_Out", 'Sales'].sum()
    dt = dt.reset_index(level=0)
    dt['Tx_Conv'] = np.round(dt['Sales']*100/dt['Link_Click'], 2)
    dt['Tx_Panier'] = np.round(dt['Panier']*100/dt['Link_Click'], 2)
    dt['Tx_Check_Out'] = np.round(dt['Check_Out']*100/dt['Link_Click'], 2)
    dt = dt.fillna(0)
    Date.append(dt)

    

    dt = df.groupby('collection')['Count'].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    dt = df.groupby('collection')["Amout_Spent", 'Link_Click','Count'].sum()
    dt = dt.reset_index(level=0)
    dt['click_for_sale'] = dt['Link_Click']/dt['Count']
    dt['Cost_for_Sale'] = dt['Amout_Spent']/dt['Count']
    dt = dt.fillna(0)
    Date.append(dt)

    dt = df[~df['collection'].isin(['None', '*'])]
    dtt = pd.DataFrame(dt.groupby(['Date ',  'collection'])["Result"].sum()).reset_index()
    dtt['Result_Cat'] = dtt['Result']
    dtt['Result_Cat'] = dtt['Result_Cat'].apply(lambda x : change_result(x))
    dt1 = pd.DataFrame(dtt[dtt['Result_Cat'] == 'Positive'].groupby(['collection'])['Result_Cat'].count()).reset_index()
    dt2 = pd.DataFrame(dtt[dtt['Result_Cat'] == 'Negative'].groupby(['collection'])['Result_Cat'].count()).reset_index()
    dt = dt1.merge(dt2, on = 'collection')
    dt = dt.fillna(0)
    dt['Pourcentage_Positive'] = np.round(dt['Result_Cat_x']*100/(dt['Result_Cat_x']+dt['Result_Cat_y']), 2)
    dt = dt.fillna(0)
    dt['Pourcentage_Negative'] = 100 - dt['Pourcentage_Positive']
    Date.append(dt)

    dt = df.groupby('Date ')['Count'].sum()
    dt = dt.reset_index(level=0)
    Date.append(dt)

    return Date


def define_graphs_collection(df, value) : 

    # convert to collection 
    df['collection'] = df['produit_Cible'].apply(lambda x : dict_collection[x] if x in dict_collection.keys() else 'None')

    
    dt = creates_set_graph_collection(df)
    
    #graph1
    fig = px.area(dt[0], x="Date ", y="CA", title="Sales Evolution", color_discrete_sequence=[color[1]])
    fig.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        height = 380,
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    #graph2
    fig2 = px.area(dt[0], x="Date ", y="Result", title="Income Evolution", color_discrete_sequence=[color[1]]) 
    fig2.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        height = 380,
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )


    #graph3
    fig3 = px.area(dt[8], x="Date ", y="Link_Click", title="Visits Evolution", color_discrete_sequence=[color[1]])
    fig3.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        height = 380,
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )    

      
    #graph4
    fig4 = px.area(dt[6], x="Date ", y="CPC", title="CPC Evolution", color_discrete_sequence=color)
    fig4.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph 5
    try :
        pourcentage = list(dt[14][['Pourcentage_Positive', 'Pourcentage_Negative']].values[0])
    except :
        pourcentage = [100, 0]
    fig5 = px.pie(values=pourcentage, names=['Win', 'Loss'], title="Product's Result", 
             color_discrete_sequence=color, hole = .7)

    fig5.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph6
    fig6 = px.area(dt[15], x="Date ", y="Count", title="Product Sale Unit Evolution", color_discrete_sequence=color)
    fig6.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph7
    data = df[df['collection'] == value]
    data = pd.DataFrame(data.groupby('produit_Cible')['Count'].sum()).reset_index()
    fig7 = px.bar(data, x = 'produit_Cible', y = 'Count', color = 'produit_Cible', color_discrete_sequence=color, title = 'Sale Per Product')
    fig7.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    #graph8
    data = df[df['collection'] == value]
    data = pd.DataFrame(data.groupby('produit_Cible')['Result'].sum()).reset_index()
    fig8 = px.bar(data, x = 'produit_Cible', y = 'Result', color = 'produit_Cible', color_discrete_sequence=color, title = 'Income Per Product')
    fig8.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    return fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8



def attribut_collection_consts(df, df1, value):

    # convert to collection 
    df['collection'] = df['produit_Cible'].apply(lambda x : dict_collection[x] if x in dict_collection.keys() else 'None')

    dt = pd.DataFrame(df.groupby('collection')['CA'].sum()).reset_index()
    total_CA = sum(dt['CA'])
    dt['Pourcentage'] = np.where(total_CA != 0, np.round(dt['CA']*100/total_CA, 2), 0)

    dt = pd.DataFrame(dt.groupby('collection')['Pourcentage'].sum()).reset_index()
    dt = dt[dt['collection'] == value]
    sale_pr = dt['Pourcentage'].item()
    
    try : 
        dt1 = pd.DataFrame(df1.groupby('collection')['CA'].sum()).reset_index()
        total_CA = sum(dt1['CA'])
        dt1['Pourcentage'] = np.where(total_CA != 0, np.round(dt1['CA']*100/total_CA, 2), 0)

        dt1 = pd.DataFrame(dt1.groupby('collection')['Pourcentage'].sum()).reset_index()
        dt1 = dt1[dt1['collection'] == value]
        sale_pr_percentage = division(sale_pr, dt1['Pourcentage'].item())
    except : 
        sale_pr_percentage = [100, '%']

    
    dt = pd.DataFrame(df.groupby('collection')['Amout_Spent'].sum()).reset_index()
    total_budget = sum(dt['Amout_Spent'])
    dt['Pourcentage'] = np.where(total_budget != 0, np.round(dt['Amout_Spent']*100/sum(dt['Amout_Spent']), 2), 0)

    dt = pd.DataFrame(dt.groupby('collection')['Pourcentage'].sum()).reset_index()
    dt = dt[dt['collection'] == value]
    budget_pr = dt['Pourcentage'].item()
    
    try : 
        dt1 = pd.DataFrame(df1.groupby('collection')['Amout_Spent'].sum()).reset_index()
        total_budget = sum(dt1['Amout_Spent'])
        dt1['Pourcentage'] = np.where(total_budget != 0, np.round(dt1['Amout_Spent']*100/total_budget, 2), 0)
        dt1 = pd.DataFrame(dt1.groupby('collection')['Pourcentage'].sum()).reset_index()
        dt1 = dt1[dt1['collection'] == value]
        budget_pr_percentage = division(sale_pr, dt1['Pourcentage'].item())
    except : 
        budget_pr_percentage = [100, '%']

    return sale_pr, sale_pr_percentage, budget_pr, budget_pr_percentage



def attribut_collection_week(df, value) :

    # convert to collection 
    df['collection'] = df['produit_Cible'].apply(lambda x : dict_collection[x] if x in dict_collection.keys() else 'None')

    dt = df.loc[df['collection'] == value]
    dt = pd.DataFrame(dt.groupby(['collection', 'Date '])['CA'].sum()).reset_index()

    max_7 = np.round(max(dt.iloc[-7:, 2]), 2)
    try : 
        max_7_percentage = division(max_7, max(dt.iloc[-8:-1, 2]))
    except : 
        max_7_percentage = [100, '%']

    max_30 = np.round(max(dt.iloc[-30:, 2]), 2)
    try : 
        max_30_percentage = division(max_30, max(dt.iloc[-31:-1, 2]))
    except : 
        max_30_percentage = [100, '%']

    max_52 = np.round(max(dt.iloc[-7*52:, 2]), 2)
    try : 
        max_52_percentage = division(max_52, max(dt.iloc[(-52*7)-1 :-1, 2]))
    except : 
        max_52_percentage = [100, '%']


    return max_7, max_7_percentage, max_30, max_30_percentage, max_52, max_52_percentage


def attribut_collection_var(df, df1):


    try : 
        visit_for_sale_tdy = np.round(sum(df['Link_Click'])/sum(df['Count']), 2)
    except : 
        visit_for_sale_tdy = 0
    try : 
        visit_forsale_percentage = division(visit_for_sale_tdy, np.round(sum(df1['Link_Click'])/sum(df1['Count']), 2))
    except : 
        visit_forsale_percentage = [100, '%']

    try :
        cost_for_sale_tdy = np.round(sum(df['Amout_Spent'])/sum(df['Count']), 2)
    except : 
        cost_for_sale_tdy = 0
    try :
        cost_percentage = division(cost_for_sale_tdy, np.round(sum(df1['Amout_Spent'])/sum(df1['Count']), 2))
    except :
        cost_percentage = [100, '%'] 

    try : 
        roas_in = np.round(sum(df['Result'])*100/sum(df['CA']), 2)
    except : 
        roas_in = 0
    try :
        roas_percentage = division(roas_in, np.round(sum(df1['Result'])*100/sum(df1['CA']), 2))
    except : 
        roas_percentage = [100, '%']

    dt = pd.DataFrame(df.groupby(['collection', 'Date '])['CA'].sum()).reset_index()
    dt1 = pd.DataFrame(df1.groupby(['collection', 'Date '])['CA'].sum()).reset_index()
    highest = np.round(max(dt['CA']),2)
    try :
        highest_percentage = division(highest, np.round(max(dt1['CA']),2))
    except : 
        highest_percentage = [100, '%']

    visit = np.round(sum(df['Link_Click']), 2)
    try : 
        visit_percentage = division(visit, np.round(sum(df1['Link_Click']), 2))
    except : 
        visit_percentage = [100, '%']

    try : 
        cpc = np.round(sum(df['Amout_Spent'])/visit, 2)
    except : 
        cpc = 0
    try :
        cpc_percentage = division(cpc, np.round(sum(df['Amout_Spent'])/sum(df1['Link_Click']), 2))
    except : 
        cpc_percentage = [100, '%']

    df['Impres'] = np.round(df['Link_Click']*100/df['CTR'])
    df = df.fillna(0)
    
    ctr = np.round(sum(df['Link_Click'])*100/sum(df['Impres']), 2) if sum(df['Impres']) != 0 else 0
    try : 
        df1['Impres'] = np.round(df1['Link_Click']*100/df1['CTR'])
        df1 = df1.fillna(0)
        ctr_percentage = division(ctr, np.round(sum(df1['Link_Click'])*100/sum(df1['Impres']), 2))
    except : 
        ctr_percentage = [100, '%']

    try : 
        cv_rate = np.round(sum(df['Sales'])*100/sum(df['Link_Click']), 2)
    except : 
        cv_rate = 0
    try :
        cv_rate_percentage = division(cv_rate, np.round(sum(df1['Sales'])*100/sum(df1['Link_Click']), 2))
    except : 
        cv_rate_percentage = [100, '%']

    return visit_for_sale_tdy, visit_forsale_percentage, cost_for_sale_tdy, cost_percentage, roas_in, roas_percentage, highest, highest_percentage, visit, visit_percentage, cpc, cpc_percentage, ctr, ctr_percentage, cv_rate, cv_rate_percentage



def attribut_collection(df, value, start, end) : 

    # convert to collection 
    df['collection'] = df['produit_Cible'].apply(lambda x : dict_collection[x] if x in dict_collection.keys() else 'None')

    max_7, max_7_percentage, max_30, max_30_percentage, max_52, max_52_percentage = attribut_collection_week(df, value)

    dt, dt1 = change_date(df, start, end)

    sale_pr, sale_pr_percentage, budget_pr, budget_pr_percentage = attribut_collection_consts(dt, dt1, value)

    dt = dt.loc[dt['collection'] == value]

    visit_for_sale_tdy, visit_forsale_percentage, cost_for_sale_tdy, cost_percentage, roas_in, roas_percentage, highest, highest_percentage, visit, visit_percentage, cpc, cpc_percentage, ctr, ctr_percentage, cv_rate, cv_rate_percentage = attribut_collection_var(dt, dt1)
    
    children = [html.Div([
                    html.Div([
                        html.Img(src = '/assets/products/' + value +'.png'),
                    ], className = 'attribut_img'),
                    html.Br(),
                    html.Div([
                        html.H3('Visit For Sale'),
                        html.H3(visit_for_sale_tdy), 
                        html.H3(visit_forsale_percentage, style = {'color' : 'rgb(255, 67, 54)'} if visit_forsale_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Cost For Sale'),
                        html.H3([cost_for_sale_tdy, ' €']), 
                        html.H3(cost_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cost_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('% Sales'),
                        html.H3([sale_pr, '%']), 
                        html.H3(sale_pr_percentage, style = {'color' : 'rgb(255, 67, 54)'} if sale_pr_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('% Budget'),
                        html.H3([budget_pr, '%']), 
                        html.H3(budget_pr_percentage, style = {'color' : 'rgb(255, 67, 54)'} if budget_pr_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Income/Sale'),
                        html.H3([roas_in, '%']), 
                        html.H4(roas_percentage, style = {'color' : 'rgb(255, 67, 54)'} if roas_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Highest Sale'),
                        html.H3([highest, ' €']), 
                        html.H3(highest_percentage, style = {'color' : 'rgb(255, 67, 54)'} if roas_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Week High/Low'),
                        html.H3([max_7, ' €']), 
                        html.H3(max_7_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if max_7_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Month High/Low'),
                        html.H3([max_30, ' €']), 
                        html.H3(max_30_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if max_30_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('52 Week High/Low'),
                        html.H3([max_52, ' €']), 
                        html.H3(max_52_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if max_52_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Visitors'),
                        html.H3(visit), 
                        html.H3(visit_percentage,  style = {'color' : 'rgb(255, 67, 54)'} if visit_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('CPC'),
                        html.H3([cpc, ' €']), 
                        html.H3(cpc_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cpc_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('CTR'),
                        html.H3([ctr, '%']), 
                        html.H3(ctr_percentage, style = {'color' : 'rgb(255, 67, 54)'} if ctr_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                    html.Div([
                        html.H3('Conversion Rate'),
                        html.H3([cv_rate, '%']), 
                        html.H3(cv_rate_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cv_rate_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                    ], className = 'attribut'),
                ], className = 'attributs')]

    return children


def best_produit(df, value, start, end) : 

    # convert to collection 
    df['collection'] = df['produit_Cible'].apply(lambda x : dict_collection[x] if x in dict_collection.keys() else 'None')

    dt, dt1 = change_date(df, start, end)

    dt = dt.loc[dt['collection'] == value]
    dt1 = dt1.loc[dt1['collection'] == value]

    dt2 = pd.DataFrame(dt.groupby('produit_Cible')['Result'].sum()).reset_index()

    top_products = dt2.sort_values(by='Result', ascending=False).head(3)

    top_product_names = top_products['produit_Cible'].tolist()

    children = [html.H1("Best 3 Products", style = {'marginTop' : '1rem', 'marginLeft' : '1rem'})]

    for name in top_product_names : 

        sale_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'CA']), sum(dt1.loc[dt1['produit_Cible'] == name, 'CA']))
        result_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Result']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Result']))
        
        try : 
            cpc = np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent'])/sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click']),2)
        except : 
            cpc = 0
        try : 
            cpc_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click'])/sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Link_Click'])/sum(dt1.loc[dt1['produit_Cible'] == name, 'Amout_Spent']))
        except : 
            cpc_percentage = [100, '%']

        try : 
            cost_sale = np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent'])/sum(dt.loc[dt['produit_Cible'] == name, 'Count']),2)
        except : 
            cost_sale = 0   
        try :    
            cost_sale_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Amout_Spent'])/sum(dt.loc[dt['produit_Cible'] == name, 'Count']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Amout_Spent'])/sum(dt1.loc[dt1['produit_Cible'] == name, 'Count']))
        except : 
            cost_sale_percentage = [100, '%']

        try : 
            conv_rate = np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Sales'])/sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click']) * 100, 2)
        except : 
            conv_rate = 0
        try :
            conv_rate_percentage = division(sum(dt.loc[dt['produit_Cible'] == name, 'Sales'])/sum(dt.loc[dt['produit_Cible'] == name, 'Link_Click']), sum(dt1.loc[dt1['produit_Cible'] == name, 'Sales'])/sum(dt1.loc[dt1['produit_Cible'] == name, 'Link_Click']))
        except : 
            conv_rate_percentage = [100, '%']


        children.append(dbc.Col([
                                html.Div([
                                    html.Img(src="/assets/products/" + name + ".png"),
                                ], className = 'attribut_img'), # Image du produit
                                html.Div([
                                    html.H2(name), # Nom du produit
                                    html.Div([
                                        html.H3("Sale"),
                                        html.H3([np.round(sum(dt.loc[dt['produit_Cible'] == name, 'CA']), 2), ' €']),
                                        html.H3(sale_percentage, style = {'color' : 'rgb(255, 67, 54)'} if sale_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Income"),
                                        html.H3([np.round(sum(dt.loc[dt['produit_Cible'] == name, 'Result']), 2), ' €']),
                                        html.H3(result_percentage, style = {'color' : 'rgb(255, 67, 54)'} if result_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Cost per click"),
                                        html.H3([cpc,  ' €']),
                                        html.H3(cpc_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cpc_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Cost per sale"),
                                        html.H3([cost_sale,  ' €']),
                                        html.H3(cost_sale_percentage, style = {'color' : 'rgb(255, 67, 54)'} if cost_sale_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                    html.Div([
                                        html.H3("Convertion rate"),
                                        html.H3([conv_rate,  '%']),
                                        html.H3(conv_rate_percentage, style = {'color' : 'rgb(255, 67, 54)'} if conv_rate_percentage[0] < 0 else {'color' : 'rgb(34, 202, 75)'}),
                                    ], className = 'best_produit'),
                                ]),
                            ], width=4))
        
    return children 



# ================== PAGE Rapport ===========================

def rapport_graph(df, start, end, value)  : 

    if  value is None or len(value) == 0 : 
        dff = df.copy()
    else : 
        dff = df.loc[df.produit_Cible.isin(value)]

    dt, dt1 = change_date(dff, start, end)

    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['CA'].sum()).reset_index()
    fig = px.bar(plot_dt[plot_dt["CA"] > 0], x="produit_Cible", y="CA", color = "produit_Cible", text='CA', color_discrete_sequence=color,
             title ='CA Per Product')
    
    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
    fig1 = px.bar(plot_dt[plot_dt["Amout_Spent"] > 0], x="produit_Cible", y="Amout_Spent", color = "produit_Cible", text='Amout_Spent', color_discrete_sequence=color,
             title ='Amount Spent Per Product')
    
    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['Result'].sum()).reset_index()
    fig2 = px.bar(plot_dt[plot_dt["Result"] != 0], x="produit_Cible", y="Result", color = "produit_Cible", text='Result', color_discrete_sequence=color,
             title ='Result Net Per Product')
    
    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['Link_Click'].sum()).reset_index()
    fig3 = px.bar(plot_dt[plot_dt["Link_Click"] > 0], x="produit_Cible", y="Link_Click", color = "produit_Cible", text='Link_Click', color_discrete_sequence=color,
             title ='Link_Click Per Product')
    
    dtt = pd.DataFrame(dt.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
    dtt = dtt[dtt['produit_Cible'] != 'None']
    dtt['Pourcentage'] = np.round(dtt['Amout_Spent']*100/sum(dtt['Amout_Spent']), 2)
    dtt.loc[dtt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dtt = pd.DataFrame(dtt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    fig4 = px.pie(dtt, values='Pourcentage', names='produit_Cible', color_discrete_sequence=color, 
                  title='Pourcentage de budget pour chaque produit')

    dtt = pd.DataFrame(dt.groupby('produit_Cible')['CA'].sum()).reset_index()
    dtt = dtt[dtt['produit_Cible'] != 'None']
    dtt['Pourcentage'] = np.round(dtt['CA']*100/sum(dt['CA']), 2)
    dtt.loc[dtt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dtt = pd.DataFrame(dtt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    fig5 = px.pie(dtt, values='Pourcentage', names='produit_Cible', color_discrete_sequence=color, 
                  title='Pourcentage de CA pour chaque produit')

    dtt = pd.DataFrame(dt.groupby('produit_Cible')['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dtt = dtt[dtt['produit_Cible'] != 'None']
    dtt['CPC'] = np.round(dtt['Amout_Spent']/dtt['Link_Click'], 2)
    fig6 = px.bar(dtt[dtt["CPC"] > 0], x="produit_Cible", y="CPC", color = "produit_Cible", text='CPC', color_discrete_sequence=color,
                  title ='CPC Par Produit')

    dtt = dt.groupby('produit_Cible')["Amout_Spent", 'Link_Click','Count'].sum()
    dtt = dtt.reset_index(level=0)
    dtt['click_for_sale'] = np.round(dtt['Link_Click']/dtt['Count'],2)
    dtt['Cost_for_Sale'] = np.round(dtt['Amout_Spent']/dtt['Count'],2)
    dtt = dtt.fillna(0)
    fig7 = px.bar(dtt[dtt["click_for_sale"] > 0], x="produit_Cible", y="click_for_sale", color = "produit_Cible", text='click_for_sale',
             color_discrete_sequence=color, title ='Click for 1 Sale')
    fig8 = px.bar(dtt[dtt["Cost_for_Sale"] > 0], x="produit_Cible", y="Cost_for_Sale", color = "produit_Cible", text='Cost_for_Sale',
             color_discrete_sequence=color, title ='Amount Spent For 1 Sale')
    
    fig.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig1.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig2.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig3.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig4.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig5.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig6.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig7.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig8.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 


    return fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8


def attribut_report(df, start, end, value) : 

    if  value is None or len(value) == 0 : 
        dff = df.copy()
    else : 
        dff = df.loc[df.produit_Cible.isin(value)]

    dt, dt1 = change_date(dff, start, end)

    ca = np.round(sum(dt['CA']),2)
    budget = np.round(sum(dt['Amout_Spent']),2)
    income = np.round(sum(dt['Result']),2)
    visits = np.round(sum(dt['Link_Click']),2)
    products = np.round(sum(dt['Count']),2)

    if sum(dt['Amout_Spent']) != 0 : 
        roas = np.round((sum(dt['CA'])/sum(dt['Amout_Spent']))*100,2)
    else : 
        roas = 100


    ca_percentage = division(ca, np.round(sum(dt1['CA']),2))
    budget_percentage = division(budget, np.round(sum(dt1['Amout_Spent']),2))
    income_percentage = division(income, np.round(sum(dt1['Result']),2))
    visits_percentage = division(visits, np.round(sum(dt1['Link_Click']),2))
    products_percentage = division(products, np.round(sum(dt1['Count']),2))
    
    if sum(dt1['Amout_Spent']) != 0 : 
        roas1 = np.round((sum(dt1['CA'])/sum(dt1['Amout_Spent']))*100,2)
    else : 
        roas1 = 100

    roas_percentage = division(roas, roas1)

    class_ca = define_class(ca_percentage[0])
    class_bduget = define_class(budget_percentage[0])
    class_income = define_class(income_percentage[0])
    class_visits = define_class(visits_percentage[0])
    class_products = define_class(products_percentage[0])
    class_roas = define_class(roas_percentage[0])

    return ca, budget, income, visits, products, roas, ca_percentage[0], budget_percentage[0], income_percentage[0], visits_percentage[0], products_percentage[0], roas_percentage[0], class_ca, class_bduget, class_income, class_visits, class_products, class_roas


def rapport_graph_exported(df, start, end, value)  : 

    if  value is None or len(value) == 0 : 
        dff = df.copy()
    else : 
        dff = df.loc[df.produit_Cible.isin(value)]

    dt, dt1 = change_date(dff, start, end)

    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['CA'].sum()).reset_index()
    fig = px.bar(plot_dt[plot_dt["CA"] > 0], x="produit_Cible", y="CA", color = "produit_Cible", text='CA', color_discrete_sequence=color,)
    
    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
    fig1 = px.bar(plot_dt[plot_dt["Amout_Spent"] > 0], x="produit_Cible", y="Amout_Spent", color = "produit_Cible", text='Amout_Spent', color_discrete_sequence=color,)
    
    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['Result'].sum()).reset_index()
    fig2 = px.bar(plot_dt[plot_dt["Result"] != 0], x="produit_Cible", y="Result", color = "produit_Cible", text='Result', color_discrete_sequence=color,)
    
    plot_dt = pd.DataFrame(dt.groupby('produit_Cible')['Link_Click'].sum()).reset_index()
    fig3 = px.bar(plot_dt[plot_dt["Link_Click"] > 0], x="produit_Cible", y="Link_Click", color = "produit_Cible", text='Link_Click', color_discrete_sequence=color,)
    
    dtt = pd.DataFrame(dt.groupby('produit_Cible')['Amout_Spent'].sum()).reset_index()
    dtt = dtt[dtt['produit_Cible'] != 'None']
    dtt['Pourcentage'] = np.round(dtt['Amout_Spent']*100/sum(dtt['Amout_Spent']), 2)
    dtt.loc[dtt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dtt = pd.DataFrame(dtt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    fig4 = px.pie(dtt, values='Pourcentage', names='produit_Cible', color_discrete_sequence=color)

    dtt = pd.DataFrame(dt.groupby('produit_Cible')['CA'].sum()).reset_index()
    dtt = dtt[dtt['produit_Cible'] != 'None']
    dtt['Pourcentage'] = np.round(dtt['CA']*100/sum(dt['CA']), 2)
    dtt.loc[dtt['Pourcentage'] < 1, 'produit_Cible'] = 'others'
    dtt = pd.DataFrame(dtt.groupby('produit_Cible')['Pourcentage'].sum()).reset_index()
    fig5 = px.pie(dtt, values='Pourcentage', names='produit_Cible', color_discrete_sequence=color, )

    dtt = pd.DataFrame(dt.groupby('produit_Cible')['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dtt = dtt[dtt['produit_Cible'] != 'None']
    dtt['CPC'] = np.round(dtt['Amout_Spent']/dtt['Link_Click'], 2)
    fig6 = px.bar(dtt[dtt["CPC"] > 0], x="produit_Cible", y="CPC", color = "produit_Cible", text='CPC', color_discrete_sequence=color,)

    dtt = dt.groupby('produit_Cible')["Amout_Spent", 'Link_Click','Count'].sum()
    dtt = dtt.reset_index(level=0)
    dtt['click_for_sale'] = np.round(dtt['Link_Click']/dtt['Count'],2)
    dtt['Cost_for_Sale'] = np.round(dtt['Amout_Spent']/dtt['Count'],2)
    dtt = dtt.fillna(0)
    fig7 = px.bar(dtt[dtt["click_for_sale"] > 0], x="produit_Cible", y="click_for_sale", color = "produit_Cible", text='click_for_sale',
             color_discrete_sequence=color)
    fig8 = px.bar(dtt[dtt["Cost_for_Sale"] > 0], x="produit_Cible", y="Cost_for_Sale", color = "produit_Cible", text='Cost_for_Sale',
             color_discrete_sequence=color)
    
    fig.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig1.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig2.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig3.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig4.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig5.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig6.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig7.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig8.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 


    return fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8


def rapport_graph_exported_long_duree(df, start, end, value)  : 

    if  value is None or len(value) == 0 : 
        dff = df.copy()
    else : 
        dff = df.loc[df.produit_Cible.isin(value)]

    dt, dt1 = change_date(dff, start, end)

    dtt = dt.groupby('Date ')["Amout_Spent", "CA", "Cout", "Result"].sum()
    dtt = dtt.reset_index(level=0)
    fig100 = go.Figure()
    fig100.add_trace(go.Scatter(x=dtt['Date '], y=dtt["Amout_Spent"],
                        mode='lines',
                        name = 'Budget',
                        marker_color=color_red[0]))
    fig100.add_trace(go.Scatter(x=dtt['Date '], y=dtt["CA"],
                        mode='lines',
                        name = "Sales",
                        marker_color=color[1]))
    fig100.add_trace(go.Scatter(x=dtt['Date '], y=dtt["Result"],
                        mode='lines',
                        name = "Income",
                        marker_color=color[0]))
    fig100.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )


    fig = px.line(dt, x = 'Date ', y = 'CA', color = "produit_Cible",
             color_discrete_sequence=color)
    fig.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    ) 

    fig1 = px.line(dt, x = 'Date ', y = 'Amout_Spent', color = "produit_Cible",
             color_discrete_sequence=color)
    fig1.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig2 = px.line(dt, x = 'Date ', y = 'Result', color = "produit_Cible",
             color_discrete_sequence=color)
    fig2.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig3 = px.line(dt, x = 'Date ', y = 'Link_Click', color = "produit_Cible",
             color_discrete_sequence=color)
    fig3.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    df1 = pd.DataFrame(dt.groupby(['Date '])['Amout_Spent'].sum()).reset_index()
    df2 = pd.DataFrame(dt.groupby(['Date ', 'produit_Cible'])['Amout_Spent'].sum()).reset_index()
    dtt = df1.merge(df2, on = 'Date ', how = 'outer')
    dtt['Pourcentage'] = np.round(dtt['Amout_Spent_y']*100/dtt['Amout_Spent_x'], 2)
    dtt['Pourcentage'] = dtt['Pourcentage'].fillna(0)
    fig4 = px.line(dtt, x = 'Date ', y = 'Pourcentage', color = "produit_Cible",
             color_discrete_sequence=color)
    fig4.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    df1 = pd.DataFrame(dt.groupby(['Date '])['CA'].sum()).reset_index()
    df2 = pd.DataFrame(dt.groupby(['Date ', 'produit_Cible'])['CA'].sum()).reset_index()
    dtt = df1.merge(df2, on = 'Date ', how = 'outer')
    dtt['Pourcentage'] = np.round(dtt['CA_y']*100/dtt['CA_x'], 2)
    dtt['Pourcentage'] = dtt['Pourcentage'].fillna(0)
    fig5 = px.line(dtt, x = 'Date ', y = 'Pourcentage', color = "produit_Cible",
             color_discrete_sequence=color)
    fig5.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    dtt = pd.DataFrame(dt.groupby(['Date ', 'produit_Cible'])['Link_Click', 'Amout_Spent'].sum()).reset_index()
    dtt['CPC'] = np.round(dtt['Amout_Spent']/dtt['Link_Click'], 2)
    dtt['CPC'] = dtt['CPC'].fillna(0)
    fig6 = px.line(dtt, x = 'Date ', y = 'CPC', color = "produit_Cible",
             color_discrete_sequence=color)
    fig6.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    dtt = dt.groupby(['Date ','produit_Cible'])["Amout_Spent", 'Link_Click','Count'].sum()
    dtt = dtt.reset_index()
    dtt['click_for_sale'] = np.round(dtt['Link_Click']/dtt['Count'],2)
    dtt['Cost_for_Sale'] = np.round(dtt['Amout_Spent']/dtt['Count'],2)
    dtt = dtt.fillna(0)
    dtt.loc[dtt['Count'] == 0, ['click_for_sale', 'Cost_for_Sale']] = 0
    fig7 = px.line(dtt, x = 'Date ', y = 'click_for_sale', color = "produit_Cible",
             color_discrete_sequence=color)
    fig7.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    fig8 = px.line(dtt, x = 'Date ', y = 'Cost_for_Sale', color = "produit_Cible",
             color_discrete_sequence=color)
    fig8.update_layout(
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        height = 380,
        paper_bgcolor= 'rgba(0, 0, 0, 0)', 
        margin=dict(
            l=20,
            r=5,
            b=5,
            t=50,
            pad=4
        ),
        legend=dict(
            font = dict(family = "Courier", size = 10, color = "black")
        ),
    )

    return fig100, fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8