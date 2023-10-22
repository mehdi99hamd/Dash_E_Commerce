import base64
import datetime
from distutils.command.upload import upload
import io
from ast import Pass

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ClientsideFunction, Input, Output, State
from dash import callback
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
import sys
import plotly.io as pio

import model

import dashboard, analysis, product, update, collection, report

info_path = r'info_product.csv'
info_data = pd.read_csv(info_path, encoding='latin-1')

dict_collection = dict(info_data[['product_name', 'collection']].values)


@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/analysis' :
        return analysis.layout
    elif pathname == '/products' :
        return product.layout
    elif pathname == '/update' :
        return update.layout
    elif pathname == '/collection' :
        return collection.layout
    elif pathname == '/Report' :
        return report.layout
    else : 
        return dashboard.layout



#====================================== DashBoard Page ===================================
@callback(Output('graph_dashboard', 'figure'),
            Output('graph_dashboard1', 'figure'),
            Output('graph_dashboard2', 'figure'),
            Output('graph_dashboard3', 'figure'),
            Output('graph_dashboard4', 'figure'),
            Output('graph_dashboard5', 'figure'),
            Output('graph_dashboard6', 'figure'),
            Output('graph_dashboard7', 'figure'),
            Output('now', 'children'),
            Output('sale', 'children'),
            Output('sale_percentage', 'children'),
            Output('sale_percentage', 'className'),
            Output('sale_cercle', 'className'),
            Output('sale_cercle_bar', 'className'),
            Output('sale_cercle_fill', 'className'),
            Output('sale_yesterday', 'children'),
            Output('budget', 'children'),
            Output('budget_percentage', 'children'),
            Output('budget_percentage', 'className'),
            Output('budget_cercle', 'className'),
            Output('budget_cercle_bar', 'className'),
            Output('budget_cercle_fill', 'className'),
            Output('budget_yesterday', 'children'),
            Output('income', 'children'),
            Output('income_percentage', 'children'),
            Output('income_percentage', 'className'),
            Output('income_cercle', 'className'),
            Output('income_cercle_bar', 'className'),
            Output('income_cercle_fill', 'className'),
            Output('income_yesterday', 'children'),
            Output('nproducts', 'children'),
            Output('nproducts_percentage', 'children'),
            Output('nproducts_percentage', 'className'),
            Output('nproducts_cercle', 'className'),     
            Output('nproducts_cercle_bar', 'className'),
            Output('nproducts_cercle_fill', 'className'),
            Output('nproducts_yesterday', 'children'),
            Output('sales-analytics', 'children'),
            
            State('data_oresli', 'data'),
            State('column_oresli', 'data'),
            Input('methode', 'value'))

def function_dashboard(data, columns, value) : 

    df = pd.DataFrame(data)
    df.columns = columns

    now, tdy_data_summed, yesterday_data_summed, column_date = model.data_today_yesterday(df, value)
    fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7 = model.define_graphs(tdy_data_summed, column_date)

    class1 = 'success'
    class2 = 'success'
    class3 = 'success'
    class4 = 'success'

    class2_bar, class2_fill, class1_bar, class1_fill, class3_bar, class3_fill, class4_bar, class4_fill = 'bar success_cercle', 'fill success_cercle', 'bar success_cercle', 'fill success_cercle', 'bar success_cercle', 'fill success_cercle', 'bar success_cercle', 'fill success_cercle'
    
    now = ['DASHBOARD E-COMMERCE : OVERVIEW ',  now]
    ca = [np.round(sum(tdy_data_summed['CA']),2)]
    budget = [np.round(sum(tdy_data_summed['Amout_Spent']),2)]
    income = [np.round(sum(tdy_data_summed['Result']),2)]
    click = [np.round(sum(tdy_data_summed['Sales']),2)]

    dict_periode = {
        'Par Mois': ' Last Month',
        'Par Jour' : ' Yesterday',
        'Par An' : ' Last Year'
    }

    ca_h = ['Compared To ', np.round(sum(yesterday_data_summed['CA']),2), ' €',  dict_periode[value]]
    res_h = ['Compared To ', np.round(sum(yesterday_data_summed['Amout_Spent']),2), ' €',  dict_periode[value]]
    sale_h = ['Compared To ', np.round(sum(yesterday_data_summed['Result']),2),  dict_periode[value]]
    click_h = ['Compared To ', np.round(sum(yesterday_data_summed['Sales']),2), dict_periode[value]]
    
    ca_pr = model.division(ca[0], np.abs(np.round(sum(yesterday_data_summed['CA']),2)))
    res_pr = model.division(budget[0], np.abs(np.round(sum(yesterday_data_summed['Amout_Spent']),2)))
    sale_pr = model.division(income[0], np.abs(np.round(sum(yesterday_data_summed['Result']),2)))
    click_pr = model.division(click[0], np.abs(np.round(sum(yesterday_data_summed['Sales']),2)))

    if click_pr[0] < 0 :
        class4 = 'danger'
        class4_bar = 'bar danger_cercle'
        class4_fill = 'fill danger_cercle'
    if sale_pr[0] < 0 :
        class3 = 'danger'
        class3_bar = 'bar danger_cercle'
        class3_fill = 'fill danger_cercle'
    if res_pr[0] < 0 :
        class2 = 'danger'
        class2_bar = 'bar danger_cercle'
        class2_fill = 'fill danger_cercle'
    if ca_pr[0] < 0 :
        class1 = 'danger'
        class1_bar = 'bar danger_cercle'
        class1_fill = 'fill danger_cercle'

    if abs(ca_pr[0]) == 100 :
        cercle_ca = 'c100 p100 petit'
    else : 
        cercle_ca = 'c100 p' + str(int(abs(ca_pr[0])%100)) + ' petit'
    if abs(res_pr[0]) == 100 :
        cercle_res = 'c100 p100 petit'
    else :
        cercle_res = 'c100 p' + str(int(abs(res_pr[0])%100)) + ' petit'
    if abs(sale_pr[0]) == 100 : 
        cercle_sale = 'c100 p100 petit'
    else : 
        cercle_sale = 'c100 p' + str(int(abs(sale_pr[0])%100)) + ' petit'
    if abs(click_pr[0]) == 100 : 
        cercle_sale = 'c100 p100 petit'
    else : 
        cercle_click = 'c100 p' + str(int(abs(click_pr[0])%100)) + ' petit'
     
    products = list(df['produit_Cible'].unique())
    if 'None' in products :
        products.remove('None')
    if '*' in products :
        products.remove('*')
    children = model.results_dashboard(products, tdy_data_summed, yesterday_data_summed)
            

    return fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, now, ca, ca_pr, class1, cercle_ca, class1_bar, class1_fill,  ca_h, budget, res_pr, class2, cercle_res, class2_bar, class2_fill, res_h, income, sale_pr, class3, cercle_sale, class3_bar, class3_fill, sale_h, click, click_pr, class4, cercle_click, class4_bar, class4_fill, click_h, children




# ================ ANALYTIC PAGE ====================

@callback(Output('graph', 'figure'),
            Output('graph2', 'figure'),
            Output('graph3', 'figure'),
            Output('graph4', 'figure'),
            Output('graph5', 'figure'),
            Output('graph6', 'figure'),
            Output('graph7', 'figure'),
            Output('graph8', 'figure'),
            Output('graph9', 'figure'),
            Output('graph10', 'figure'),
            Output('graph11', 'figure'),
            Output('graph12', 'figure'),
            Output('graph13', 'figure'),
            Output('graph14', 'figure'),

            Output('sale_analysis', 'children'),
            Output('sale_analysis_percentage', 'children'),
            Output('sale_analysis_percentage', 'className'),
            Output('budget_analysis', 'children'),
            Output('budget_analysis_percentage', 'children'),
            Output('budget_analysis_percentage', 'className'),
            Output('income_analysis', 'children'),
            Output('income_analysis_percentage', 'children'),
            Output('income_analysis_percentage', 'className'),
            Output('visit_analysis', 'children'),
            Output('visit_analysis_percentage', 'children'),
            Output('visit_analysis_percentage', 'className'),
            Output('products_analysis', 'children'),
            Output('products_analysis_percentage', 'children'),
            Output('products_analysis_percentage', 'className'),
            Output('roas_analysis', 'children'),
            Output('roas_analysis_percentage', 'children'),
            Output('roas_analysis_percentage', 'className'),

            Output('best_3_products_analyis', 'children'),

            State('data_oresli', 'data'),
            State('column_oresli', 'data'),
            Input('date_analysis', 'start_date'),
            Input('date_analysis', 'end_date'),
            Input('produits_chosen', 'value'))

def update_analysis(data, columns, start, end, value) : 

    df = pd.DataFrame(data)
    df.columns = columns

    if  value is None or len(value) == 0 : 
        dt = df.copy()
    else : 
        dt = df.loc[df.produit_Cible.isin(value)]
    
    
    dt1 = dt.copy()

    if start is not None and end is not None:
        dt = dt.loc[(start <= dt['Date ']) & (dt['Date '] <= end)]
        n_days = len(dt['Date '].unique())
        end = start
        start = str(datetime.strptime(start, "%Y-%m-%d") -  timedelta(days=n_days))[:10]
        dt1 = dt1.loc[(start <= dt1['Date ']) & (dt1['Date '] <= end)]
    else :
        dt1 = pd.DataFrame(columns=dt.columns)

    if len(dt1) == 0 :
        dt1 = dt.copy()
        for col in dt1.columns:
            dt1[col].values[:] = 0

    
    children = model.best_produit_analysis(dt, dt1)

    ca = np.round(sum(dt['CA']),2)
    budget = np.round(sum(dt['Amout_Spent']),2)
    income = np.round(sum(dt['Result']),2)
    visits = np.round(sum(dt['Link_Click']),2)
    products = np.round(sum(dt['Count']),2)

    if sum(dt['Amout_Spent']) != 0 : 
        roas = np.round((sum(dt['CA'])/sum(dt['Amout_Spent']))*100,2)
    else : 
        roas = 100


    ca_percentage = model.division(ca, np.round(sum(dt1['CA']),2))
    budget_percentage = model.division(budget, np.round(sum(dt1['Amout_Spent']),2))
    income_percentage = model.division(income, np.round(sum(dt1['Result']),2))
    visits_percentage = model.division(visits, np.round(sum(dt1['Link_Click']),2))
    products_percentage = model.division(products, np.round(sum(dt1['Count']),2))
    
    if sum(dt1['Amout_Spent']) != 0 : 
        roas1 = np.round((sum(dt1['CA'])/sum(dt1['Amout_Spent']))*100,2)
    else : 
        roas1 = 100

    roas_percentage = model.division(roas, roas1)

    class_ca = model.define_class(ca_percentage[0])
    class_bduget = model.define_class(budget_percentage[0])
    class_income = model.define_class(income_percentage[0])
    class_visits = model.define_class(visits_percentage[0])
    class_products = model.define_class(products_percentage[0])
    class_roas = model.define_class(roas_percentage[0])


    fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13, fig14 = model.define_graphs_analysis(dt)

    return fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13, fig14, ca, ca_percentage, class_ca, budget, budget_percentage, class_bduget, income, income_percentage, class_income, visits, visits_percentage, class_visits, products, products_percentage, class_products, roas, roas_percentage, class_roas, children




# ============= Page Products =============================

@callback(Output('graph_products', 'figure'),
            Output('graph_products2', 'figure'),
            Output('graph_products3', 'figure'),
            Output('graph_products4', 'figure'),
            Output('graph_products5', 'figure'),
            Output('graph_products6', 'figure'),

            Output('products_title', 'children'),

            Output('sale_products', 'children'),
            Output('sale_products_percentage', 'children'),
            Output('sale_products_percentage', 'className'),
            Output('budget_products', 'children'),
            Output('budget_products_percentage', 'children'),
            Output('budget_products_percentage', 'className'),
            Output('income_products', 'children'),
            Output('income_products_percentage', 'children'),
            Output('income_products_percentage', 'className'),
            Output('visits_products', 'children'),
            Output('visits_products_percentage', 'children'),
            Output('visits_products_percentage', 'className'),
            Output('products_products', 'children'),
            Output('products_products_percentage', 'children'),
            Output('products_products_percentage', 'className'),
            Output('roas_products', 'children'),
            Output('roas_products_percentage', 'children'),
            Output('roas_products_percentage', 'className'),

            Output('info_products', 'children'),

            State('data_oresli', 'data'),
            State('column_oresli', 'data'),
            Input('date_products', 'start_date'),
            Input('date_products', 'end_date'),
            Input('produits_chosen_products', 'value'))

def update_products(data, columns, start, end, value):

    df = pd.DataFrame(data)
    df.columns = columns

    children = model.attribut_products(df, value, start, end)

    dt = df.loc[df['produit_Cible'] == value]

    dt, dt1 = model.change_date(dt, start, end)

    title = value

    ca = np.round(sum(dt['CA']),2)
    budget = np.round(sum(dt['Amout_Spent']),2)
    income = np.round(sum(dt['Result']),2)
    visits = np.round(sum(dt['Link_Click']),2)
    products = np.round(sum(dt['Count']),2)

    if sum(dt['Amout_Spent']) != 0 : 
        roas = np.round((sum(dt['CA'])/sum(dt['Amout_Spent']))*100,2)
    else : 
        roas = 100


    ca_percentage = model.division(ca, np.round(sum(dt1['CA']),2))
    budget_percentage = model.division(budget, np.round(sum(dt1['Amout_Spent']),2))
    income_percentage = model.division(income, np.round(sum(dt1['Result']),2))
    visits_percentage = model.division(visits, np.round(sum(dt1['Link_Click']),2))
    products_percentage = model.division(products, np.round(sum(dt1['Count']),2))
    
    if sum(dt1['Amout_Spent']) != 0 : 
        roas1 = np.round((sum(dt1['CA'])/sum(dt1['Amout_Spent']))*100,2)
    else : 
        roas1 = 100

    roas_percentage = model.division(roas, roas1)

    class_ca = model.define_class(ca_percentage[0])
    class_bduget = model.define_class(budget_percentage[0])
    class_income = model.define_class(income_percentage[0])
    class_visits = model.define_class(visits_percentage[0])
    class_products = model.define_class(products_percentage[0])
    class_roas = model.define_class(roas_percentage[0])

    fig, fig2, fig3, fig4, fig5, fig6 = model.define_graphs_products(dt)

    return fig, fig2, fig3, fig4, fig5, fig6, title, ca, ca_percentage, class_ca, budget, budget_percentage, class_bduget, income, income_percentage, class_income, visits, visits_percentage, class_visits, products, products_percentage, class_products, roas, roas_percentage, class_roas, children


# ====================== Page Update =============================

@callback( Output('data_oresli', 'data'),
              Output('column_oresli', 'data'),
              Output('start', 'n_clicks'),
              Output('update', 'children'),
              Output('update', 'className'),
              State('data_oresli', 'data'),
              State('column_oresli', 'data'),
              State('info_pro', 'data'),
              State('column_info', 'data'),
              State('upload-data_google', 'contents'),
              State('upload-data_google', 'filename'),
              State('upload-data_sales', 'contents'),
              State('upload-data_sales', 'filename'),
              State('upload-data_visit', 'contents'),
              State('upload-data_visit', 'filename'),
              Input('start', 'n_clicks'))

def update_output1(data, column, info_data, info_colu, contents1, filename1, contents2, filename2, contents3, filename3, click):
    
    oresli =  pd.DataFrame(data)
    oresli.columns = column

    info_data =  pd.DataFrame(info_data)
    info_data.columns = info_colu

    children = []
    class_update = 'update_text'

    if contents1 is not None and contents2 is not None and contents3 is not None and click > 0 :
        if ('csv' in filename1  or "xlsx" in filename1) and ('csv' in filename2  or "xlsx" in filename2) and ('csv' in filename3  or "xlsx" in filename3):
            df1 = model.parse_contents(contents1, filename1)
            df2 = model.parse_contents(contents2, filename2)
            df3 = model.parse_contents(contents3, filename3)
            df = model.update_google(df1, df3, df2, filename1, filename3, filename2, info_data)
            oresli = pd.concat([oresli, df])
            path = 'oresli.csv'
            oresli.to_csv(path, index=False)
            children = ['Update Completed !']
            click = 0
            return  oresli.values, oresli.columns, click, children, class_update
        else :
            children = ['Please Select a .csv or .xlsx File']
            class_update = 'rouge'
            click = 0
            return  oresli.values, oresli.columns, click, children, class_update
    else : 
        return  oresli.values, oresli.columns, click, children, class_update



@callback(Output('update_product', 'children'),
              Output('update_product', 'className'),
              Output('info_pro', 'data'),
              Output('column_info', 'data'),
              State('info_pro', 'data'),
              State('column_info', 'data'),
              Input('upload-data_add_product', 'contents'),
              State('upload-data_add_product', 'filename'))

def update_output1(data, columns, contents1, filename1):
    children = []
    class_update = 'update_text'
    if contents1 is not None  :
        if ('csv' in filename1  or "xlsx" in filename1) :
            df1 = model.parse_contents1(contents1, filename1)
            info_data_new = pd.DataFrame(df1)
            info_data_new.columns = columns
            path = 'info_product.csv'
            info_data_new.to_csv(path, index=False)
            data = info_data_new.values
            columns = info_data_new.columns
            children = ['Update Products Completed !']
            return  children, class_update, data, columns
        else :
            children = ['Please Select a .csv or .xlsx File']
            class_update = 'rouge'
            return  children, class_update, data, columns
    else : 
        return  children, class_update, data, columns
    



# ============= Page Collection =============================

@callback(Output('graph_collection', 'figure'),
            Output('graph_collection2', 'figure'),
            Output('graph_collection3', 'figure'),
            Output('graph_collection4', 'figure'),
            Output('graph_collection5', 'figure'),
            Output('graph_collection6', 'figure'),
            Output('graph_collection7', 'figure'),
            Output('graph_collection8', 'figure'),

            Output('collection_title', 'children'),

            Output('sale_collection', 'children'),
            Output('sale_collection_percentage', 'children'),
            Output('sale_collection_percentage', 'className'),
            Output('budget_collection', 'children'),
            Output('budget_collection_percentage', 'children'),
            Output('budget_collection_percentage', 'className'),
            Output('income_collection', 'children'),
            Output('income_collection_percentage', 'children'),
            Output('income_collection_percentage', 'className'),
            Output('visits_collection', 'children'),
            Output('visits_collection_percentage', 'children'),
            Output('visits_collection_percentage', 'className'),
            Output('products_collection', 'children'),
            Output('products_collection_percentage', 'children'),
            Output('products_collection_percentage', 'className'),
            Output('roas_collection', 'children'),
            Output('roas_collection_percentage', 'children'),
            Output('roas_collection_percentage', 'className'),

            Output('info_collection', 'children'),

            Output('best_3_products', 'children'),

            State('data_oresli', 'data'),
            State('column_oresli', 'data'),
            Input('date_collection', 'start_date'),
            Input('date_collection', 'end_date'),
            Input('produits_chosen_collection', 'value'))

def update_collection(data, columns, start, end, value):

    df = pd.DataFrame(data)
    df.columns = columns

    children = model.attribut_collection(df, value, start, end)

    children_best_product = model.best_produit(df, value, start, end)

    df['collection'] = df['produit_Cible'].apply(lambda x : dict_collection[x] if x in dict_collection.keys() else 'None')
    dt = df.loc[df['collection'] == value]

    dt, dt1 = model.change_date(dt, start, end)

    title = value

    ca = np.round(sum(dt['CA']),2)
    budget = np.round(sum(dt['Amout_Spent']),2)
    income = np.round(sum(dt['Result']),2)
    visits = np.round(sum(dt['Link_Click']),2)
    products = np.round(sum(dt['Count']),2)

    if sum(dt['Amout_Spent']) != 0 : 
        roas = np.round((sum(dt['CA'])/sum(dt['Amout_Spent']))*100,2)
    else : 
        roas = 100


    ca_percentage = model.division(ca, np.round(sum(dt1['CA']),2))
    budget_percentage = model.division(budget, np.round(sum(dt1['Amout_Spent']),2))
    income_percentage = model.division(income, np.round(sum(dt1['Result']),2))
    visits_percentage = model.division(visits, np.round(sum(dt1['Link_Click']),2))
    products_percentage = model.division(products, np.round(sum(dt1['Count']),2))
    
    if sum(dt1['Amout_Spent']) != 0 : 
        roas1 = np.round((sum(dt1['CA'])/sum(dt1['Amout_Spent']))*100,2)
    else : 
        roas1 = 100

    roas_percentage = model.division(roas, roas1)

    class_ca = model.define_class(ca_percentage[0])
    class_bduget = model.define_class(budget_percentage[0])
    class_income = model.define_class(income_percentage[0])
    class_visits = model.define_class(visits_percentage[0])
    class_collection = model.define_class(products_percentage[0])
    class_roas = model.define_class(roas_percentage[0])

    fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8 = model.define_graphs_collection(dt, value)

    return fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8, title, ca, ca_percentage, class_ca, budget, budget_percentage, class_bduget, income, income_percentage, class_income, visits, visits_percentage, class_visits, products, products_percentage, class_collection, roas, roas_percentage, class_roas, children, children_best_product



#====================================== Report Page ===================================

@callback(Output('graph_report', 'figure'),
            Output('graph_report1', 'figure'),
            Output('graph_report2', 'figure'),
            Output('graph_report3', 'figure'),
            Output('graph_report4', 'figure'),
            Output('graph_report5', 'figure'),
            Output('graph_report6', 'figure'),
            Output('graph_report7', 'figure'),
            Output('graph_report8', 'figure'),

            State('data_oresli', 'data'),
            State('column_oresli', 'data'),
            Input('date_report', 'start_date'),
            Input('date_report', 'end_date'),
            Input('produits_report', 'value'))

def update_report(data, columns, start, end, value):

    df = pd.DataFrame(data)
    df.columns = columns

    fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8 = model.rapport_graph(df, start, end, value)

    return fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8 



@callback(
        Output('export', 'children'),
        Output('export-button', 'n_clicks'),
        Input('export-button', 'n_clicks'),
        State('data_oresli', 'data'),
        State('column_oresli', 'data'),
        State('date_report', 'start_date'),
        State('date_report', 'end_date'),
        State('produits_report', 'value')
)
def export_report(n_clicks, data, columns, start, end, value): # Ajoutez les arguments pour d'autres figures
    children = []

    if n_clicks > 0:

        content = '''<link rel="stylesheet" href="style_report.css">'''
        content += '''<link rel="stylesheet" href="style_mini_chart.css">'''

        date_format = "%Y-%m-%d"  # Assumant que vos dates sont sous le format "YYYY-MM-DD"
        start_date = datetime.strptime(start, date_format).date()
        end_date = datetime.strptime(end, date_format).date()

        # Calculer la différence
        difference = end_date - start_date

        df = pd.DataFrame(data)
        df.columns = columns

        fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8 = model.rapport_graph_exported(df, start, end, value)

        ca, budget, income, visits, products, roas, ca_percentage, budget_percentage, income_percentage, visits_percentage, products_percentage, roas_percentage, class_ca, class_bduget, class_income, class_visits, class_products, class_roas =  model.attribut_report(df, start, end, value)

        if difference >= timedelta(days=3) : 
           fig100, fig10, fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18 = model.rapport_graph_exported_long_duree(df, start, end, value)


        # Vérifier si la différence est d'un jour
        if difference == timedelta(days=1):
            content += f"<h1>Business Report of " + str(start) + " </h1>"
        else : 
            content += f"<h1>Business Report between " + str(start) + " and " + str(end) + " </h1>"


        content += '''<div class="row align-items-center">
                        <div class="card">
                            <div class = "card_body">
                                <h2>Sales</h2>
                                <h3>''' + str(ca) + '''</h3>
                            </div>
                            <div class = "card_body">
                                <div class="sparks dotline-extrathick">{30,60,90,60,100,50,45,20}</div>
                                <small class=''' + class_ca + '''>'''  + str(ca_percentage) + ''' %</small>
                            </div>
                        </div>
                        <div class="card">
                            <div class = "card_body">
                                <h2>Budget</h2>
                                <h3>''' + str(budget) + '''</h3>
                            </div>
                            <div class = "card_body">    
                                <div class="sparks dotline-extrathick">{30,60,90,60,100,50,45,20}</div>
                                <small class=''' + class_bduget + '''>'''  + str(budget_percentage) + ''' %</small>
                            </div>
                        </div>
                        <div class="card">
                            <div class = "card_body">
                                <h2>Incomes</h2>
                                <h3>'''+ str(income) + '''</h3>
                            </div>
                            <div class = "card_body">    
                                <div class="sparks dotline-extrathick">{30,60,90,60,100,50,45,20}</div>
                                <small class=''' + class_income + '''>'''  + str(income_percentage) + ''' %</small>
                            </div>    
                        </div>
                        <div class="card">
                            <div class = "card_body">
                                <h2>Visitors</h2>
                                <h3>'''+ str(visits) + '''</h3>
                            </div>
                            <div class = "card_body">
                                <div class="sparks sparks bar-extrawide">{30,60,90,60,100,50,45,20}</div>
                                <small class=''' + class_visits + '''>'''  + str(visits_percentage) + ''' %</small>
                            </div>    
                        </div>
                        <div class="card">
                            <div class = "card_body">
                                <h2>Products</h2>
                                <h3>'''+ str(products) + '''</h3>
                            </div>
                            <div class = "card_body">
                                <div class="sparks sparks bar-extrawide">{30,60,90,60,100,50,45,20}</div>
                                <small class=''' + class_products + '''>'''  + str(products_percentage) + ''' %</small>
                            </div>
                        </div>
                        <div class="card">
                            <div class = "card_body">
                                <h2>ROAS</h2>
                                <h3>''' + str(roas) + '''</h3>
                            </div>
                            <div class = "card_body">
                                <div class="sparks sparks bar-extrawide">{30,60,90,60,100,50,45,20}</div>
                                <small class='''  + str(class_roas) + ''' %>'''  + str(roas_percentage) + ''' %</small>
                            </div>
                        </div>
                    </div>'''
        
        # Combinez le titre et le contenu des graphes pour créer le rapport HTML
        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution Of Sales, Budget And Income</<h2>"
            content += "</br>"
            content += pio.to_html(fig100, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Sales Per Product</<h2>"
        content += "</br>"
        content += pio.to_html(fig, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution Of Sales Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig10, full_html=False)


        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Amount Spent Per Product</<h2>"
        content += "</br>"
        content += pio.to_html(fig1, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution Amount Spent Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig11, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Net Profit Per Product</<h2>"
        content += "</br>"
        content += pio.to_html(fig2, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution Of Net Profit Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig12, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Click Per Product</<h2>"
        content += "</br>"
        content += pio.to_html(fig3, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution Clicks Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig13, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Percentage Of Expenditure On Each Product</<h2>"
        content += "</br>"
        content += pio.to_html(fig4, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution Pourcentage Amount Spent Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig14, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Percentage of Revenue for Each Product</<h2>"
        content += "</br>"
        content += pio.to_html(fig5, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution Pourcentage Revenue Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig15, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Cost Per Click Per Product</<h2>"
        content += "</br>"
        content += pio.to_html(fig6, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution CPC Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig16, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Click for 1 Sale</<h2>"
        content += "</br>"
        content += pio.to_html(fig7, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution For Click/Sale Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig17, full_html=False)

        content += "</br>"
        content += "</br>"
        content += "<h2 class = 'title_graph'>Amount Spent For 1 Sale</<h2>"
        content += "</br>"
        content += pio.to_html(fig8, full_html=False)

        if difference >= timedelta(days=3) : 
            content += "</br>"
            content += "</br>"
            content += "<h2 class = 'title_graph'>Evolution For Amount Spent/Sale Per Product</<h2>"
            content += "</br>"
            content += pio.to_html(fig18, full_html=False)

        content += "</br>"
        content += "</br>"
        
        # Définir le chemin et le nom de fichier pour le rapport
        path = r"D:\e-comm\Siffect\projet2\rapport"

        if difference == timedelta(days=1):
            file_path = os.path.join(path, "rapport_" + str(start) + ".html")
        else : 
            file_path = os.path.join(path, "rapport_" + str(start) + "_" + str(end) + ".html")
        
        # Écrire le contenu dans le fichier HTML
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        n_clicks = 0

        children = ['Report Exported !']

        return children, n_clicks
    
    else :
        return children, n_clicks