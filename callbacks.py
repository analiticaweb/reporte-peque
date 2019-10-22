from dash.dependencies import Input, Output
from app import app
import plotly.graph_objs as go
from plotly import tools

from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime

import numpy as np
import pandas as pd

import io
import flask
from flask import send_file

from components import update_graph_scatter, update_graph_pie, temp_var
from components import make_dash_table


pd.options.mode.chained_assignment = None

# Read in Travel Report Data
# Ingreso de claves - Carga de datos

string_months = {1:'Enero',2:'Febrero',3:'Marzo', 4:'Abril',5:'Mayo',6:'Junio', 7:'Julio',
                 8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre',}

cat_direc = {'PA?ALES':'Pañales','PA?ITOS':'Pañitos','CREMITAS':'Cremitas','OTROS':'Otros','CUPONES':'Cupones'}

colors = ['#9079b7','#4179bd','#00a94f','#ffd200','#00a6cb','#0d5409','#d77233','#bdefdd','#efba7b']

dir_medio_insc = {'Actividad Toallitas':'Actividades', 'App Pequenin':'App',
                 'Automatizacion De Sedes Pequenin':'Automatizacion Sedes','Barriguitas Temporada 2':'Actividades',
                 'Cadena':'Cadena','Call Center Multienlace':'Call Center','Dia de la madre 2019':'Actividades','Dia de la mujer 2019':'Actividades',
                 'Dia del ni?o 2019':'Actividades','Dia del ni?o Ecuador 2019':'Actividades',
                 'Facebook Pequenin Colombia':'Facebook','Sitio Web Pequenin':'Sitio Web',
                 'Sitio Web Pequenin Bolivia':'Fuera de Colombia','Sitio Web Pequenin Ecuador':'Fuera de Colombia',
                 'Sitio Web Pequenin Republica Dominicana':'Fuera de Colombia'
                 }

dir_etapas = {'embarazada':1, 'recien nacido':2, 'acostadito':3, 'explorador':4, 'aventurero':5,
              '36 o mayor':6}

num_seg_dir = {'Oro':1,'Plata':2,'Bronce':3}

############################ Start carga datos Registros ############################
# Ingreso de claves - Carga de datos
df_registros = pd.read_csv("data/df_registros.csv")
# Variables temporales
df_registros["DATE"] = pd.to_datetime(df_registros["FECHA_INSCRIPCION"])
df_registros["MONTH"] = df_registros["DATE"].dt.month
df_registros["YEAR"] = df_registros["DATE"].dt.year
df_registros["DAY"] = df_registros["DATE"].dt.day

df_primer = pd.read_csv("data/df_primer_contacto.csv")
# Variables temporales
df_primer["DATE"] = pd.to_datetime(df_primer["FECHA_PRIMER_CONTACTO"])
df_primer["MONTH"] = df_primer["DATE"].dt.month
df_primer["YEAR"] = df_primer["DATE"].dt.year
df_primer["DAY"] = df_primer["DATE"].dt.day

df_activas = pd.read_csv("data/df_activas.csv")
############################ End carga datos Claves ############################


############################ Start carga datos Claves ############################
# Ingreso de claves - Carga de datos
## por categorías
df_claves_cat = pd.read_csv("data/df_claves_cat.csv")
# Variables temporales
df_claves_cat = temp_var(df=df_claves_cat)
## Por medio
df_claves_med = pd.read_csv("data/df_claves_med.csv")
# Variables temporales
df_claves_med = temp_var(df=df_claves_med)
# Clasificacion claves
df_clasificacion_claves = pd.read_csv("data/df_clasificacion_claves.csv")
############################ End carga datos Claves ############################

############################ Start carga datos Redenciones ############################

#Por lugar de compra
df_red_lug = pd.read_csv('data/df_red_lug.csv')
#Por tipo de producto
df_red_tipo = pd.read_csv('data/df_red_tipo.csv')
# Variables temporales
df_red_lug = temp_var(df=df_red_lug)
# Variables temporales
df_red_tipo = temp_var(df=df_red_tipo)

############################ End carga datos Redenciones ############################

############################ Start carga datos Portal ############################

#Por lugar de compra
df_portal_diario = pd.read_csv('data/df_portal_diario.csv')
df_portal_diario['Avg. session length (min)'] = df_portal_diario['Avg. session length (min)'].astype(str).str.replace(',','.').astype(float)
df_portal_diario['Bounce rate'] = df_portal_diario['Bounce rate'].astype(str).str.replace(',','.').astype(float)

df_portal_mensual = pd.read_csv('data/df_portal_mensual.csv')
df_portal_mensual['Avg. session length (min)'] = df_portal_mensual['Avg. session length (min)'].astype(str).str.replace(',','.').astype(float)
df_portal_mensual['Bounce rate'] = df_portal_mensual['Bounce rate'].astype(str).str.replace(',','.').astype(float)
############################ End carga datos Portal ############################



######################## START Análitico de REGISTROS Callbacks ########################
@app.callback(Output('dropdown-distritos-registros', 'value'),
	[Input('items-options-distrito-registros', 'value')])
def update_dropdown_distritos(option):
    if option == 'TODOS':
        return ['CUNDI-BOY','ANTIOQUIA','CENTRO','PACIFICO', 'OTROS', 'ATLANTICO', 'SANTANDERES', 'EJE CAFETERO',
                'LLANOS','OTRO']
    else:
        return []

#### Date Picker Callback
@app.callback(Output('output-container-date-picker-registros', 'children'),
	[Input('my-date-picker-range-registros', 'start_date'),
	 Input('my-date-picker-range-registros', 'end_date')])
def update_output(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    number_days = (end_date - start_date).days
    return 'Se seleccionaron '+str(number_days)+' días'

#### Update graph mensual Callback
@app.callback(
    Output('registros-mes', 'figure'),
    [Input('my-date-picker-range-registros', 'start_date'),
     Input('my-date-picker-range-registros', 'end_date'),
     Input('items-options-total_registros_primer', 'value'),
     Input('dropdown-distritos-registros', 'value')])
def update_graph_mes(start_date, end_date,option,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    if option=='TOT':
        filtered_df_1 = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
        filtered_df_1 = filtered_df_1.drop_duplicates(subset="VISITORID").reset_index()
        filtered_df_1 = filtered_df_1[filtered_df_1["PAIS"]=='COLOMBIA'].reset_index(drop=True)
        filtered_df_1 = filtered_df_1[filtered_df_1["DISTRITO"].isin(distritos)]
        filtered_df_1 = filtered_df_1.groupby(by=["YEAR","MONTH"]).agg({'VISITORID':'count'}).reset_index()
        filtered_df_1['MONTH'] = filtered_df_1['MONTH'].map(string_months)

        filtered_df_2 = df_primer[df_primer.FECHA_PRIMER_CONTACTO.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
        filtered_df_2 = filtered_df_2.drop_duplicates(subset="ID").reset_index()
        filtered_df_2 = filtered_df_2[filtered_df_2["DISTRITO"].isin(distritos)]
        filtered_df_2 = filtered_df_2.groupby(by=["YEAR","MONTH"]).agg({'ID':'nunique'}).reset_index()
        filtered_df_2['MONTH'] = filtered_df_2['MONTH'].map(string_months)

        filtered_df = pd.merge(left=filtered_df_1,right=filtered_df_2,on=['YEAR','MONTH'],how='left')
        filtered_df['VISITORID'] = filtered_df['VISITORID'].fillna(0)
        filtered_df['ID'] = filtered_df['ID'].fillna(0)
        filtered_df['TOT'] = filtered_df['VISITORID']+filtered_df['ID']
        column = 'TOT'

    elif option=='REGISTROS':
        filtered_df = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
        filtered_df = filtered_df.drop_duplicates(subset="VISITORID").reset_index()
        filtered_df = filtered_df[filtered_df["PAIS"]=='COLOMBIA'].reset_index(drop=True)
        filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
        filtered_df = filtered_df.groupby(by=["YEAR","MONTH"]).agg({'VISITORID':'count'}).reset_index()
        filtered_df['MONTH'] = filtered_df['MONTH'].map(string_months)
        column = 'VISITORID'
    else:
        filtered_df = df_primer[df_primer.FECHA_PRIMER_CONTACTO.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
        filtered_df = filtered_df.drop_duplicates(subset="ID").reset_index()
        filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
        filtered_df = filtered_df.groupby(by=["YEAR","MONTH"]).agg({'ID':'nunique'}).reset_index()
        filtered_df['MONTH'] = filtered_df['MONTH'].map(string_months)
        column = 'ID'

    return update_graph_scatter(df=filtered_df,column=column,per="MONTH")

#### Update graph diaria Callback
@app.callback(
    Output('registros-dia', 'figure'),
    [Input('my-date-picker-range-registros', 'start_date'),
     Input('my-date-picker-range-registros', 'end_date'),
     Input('items-options-total_registros_primer', 'value'),
     Input('dropdown-distritos-registros', 'value')])
def update_graph_dia(start_date, end_date,option,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]

    #CONDINCIÓN DE DISTRITOS
    if distritos==[]:
        month = 0
    else:
        month = int(filtered_df.DATE.max().month)

    #TOTAL, SOLO REGISTROS, O PRIMER CONTACTO
    if option=='TOT':
        filtered_df_1 = filtered_df.drop_duplicates(subset="VISITORID").reset_index()
        filtered_df_1 = filtered_df_1[filtered_df_1["PAIS"]=='COLOMBIA'].reset_index(drop=True)
        filtered_df_1 = filtered_df_1[filtered_df_1["DISTRITO"].isin(distritos)]
        filtered_df_1 = filtered_df_1[filtered_df_1["MONTH"].astype(int)==month].reset_index(drop=True)
        filtered_df_1["MONTH"] = filtered_df_1["MONTH"].map(string_months)
        filtered_df_1 = filtered_df_1.groupby(by=["YEAR","MONTH","DAY"]).agg({'VISITORID':'nunique'}).reset_index()
        filtered_df_1["DAY"] = filtered_df_1["MONTH"] + "-" + filtered_df_1["DAY"].astype(str)

        filtered_df_2 = df_primer[df_primer.FECHA_PRIMER_CONTACTO.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
        filtered_df_2 = filtered_df_2.drop_duplicates(subset='ID').reset_index()
        filtered_df_2 = filtered_df_2[filtered_df_2["DISTRITO"].isin(distritos)]
        filtered_df_2 = filtered_df_2[filtered_df_2["MONTH"].astype(int)==month].reset_index(drop=True)
        filtered_df_2["MONTH"] = filtered_df_2["MONTH"].map(string_months)
        filtered_df_2 = filtered_df_2.groupby(by=["YEAR","MONTH","DAY"]).agg({'ID':'nunique'}).reset_index()
        filtered_df_2["DAY"] = filtered_df_2["MONTH"] + "-" + filtered_df_2["DAY"].astype(str)

        filtered_df = pd.merge(left=filtered_df_1,right=filtered_df_2,on=['YEAR','MONTH','DAY'],how='left')
        filtered_df['VISITORID'] = filtered_df['VISITORID'].fillna(0)
        filtered_df['ID'] = filtered_df['ID'].fillna(0)
        filtered_df['TOT'] = filtered_df['VISITORID']+filtered_df['ID']
        column = 'TOT'

    elif option=='REGISTROS':
        filtered_df = filtered_df.drop_duplicates(subset="VISITORID").reset_index()
        filtered_df = filtered_df[filtered_df["PAIS"]=='COLOMBIA'].reset_index(drop=True)
        filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
        filtered_df = filtered_df[filtered_df["MONTH"].astype(int)==month].reset_index(drop=True)
        filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
        filtered_df = filtered_df.groupby(by=["YEAR","MONTH","DAY"]).agg({'VISITORID':'nunique'}).reset_index()
        filtered_df["DAY"] = filtered_df["MONTH"] + "-" + filtered_df["DAY"].astype(str)
        column = 'VISITORID'
    else:
        filtered_df = df_primer[df_primer.FECHA_PRIMER_CONTACTO.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
        filtered_df = filtered_df.drop_duplicates(subset='ID').reset_index()
        filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
        filtered_df = filtered_df[filtered_df["MONTH"].astype(int)==month].reset_index(drop=True)
        filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
        filtered_df = filtered_df.groupby(by=["YEAR","MONTH","DAY"]).agg({'ID':'nunique'}).reset_index()
        filtered_df["DAY"] = filtered_df["MONTH"] + "-" + filtered_df["DAY"].astype(str)
        column = 'ID'

    return update_graph_scatter(df=filtered_df,column=column,per="DAY")

#### Callback for total table
@app.callback(Output('total-table-registros', 'data'),
	[Input('my-date-picker-range-registros', 'start_date'),
	 Input('my-date-picker-range-registros', 'end_date'),
     Input('dropdown-distritos-registros', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df_1 = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df_1 = filtered_df_1.drop_duplicates(subset="VISITORID").reset_index()
    filtered_df_1 = filtered_df_1[filtered_df_1["PAIS"]=='COLOMBIA'].reset_index(drop=True)
    filtered_df_1 = filtered_df_1[filtered_df_1["DISTRITO"].isin(distritos)]


    filtered_df_2 = df_primer[df_primer.FECHA_PRIMER_CONTACTO.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df_2 = filtered_df_2.drop_duplicates(subset='ID').reset_index()
    filtered_df_2 = filtered_df_2[filtered_df_2["DISTRITO"].isin(distritos)]


    filtered_df = pd.merge(left=filtered_df_1,right=filtered_df_2,on=['YEAR','MONTH','DAY'],how='left')
    filtered_df['VISITORID'] = filtered_df['VISITORID'].fillna(0)
    filtered_df['ID'] = filtered_df['ID'].fillna(0)
    filtered_df['TOT'] = filtered_df['VISITORID']+filtered_df['ID']

    registros = filtered_df_1['VISITORID'].count()
    primer_contacto = filtered_df_2['ID'].count()
    total = registros + primer_contacto
    return [{'Indicador':'Registros nuevos','Total':registros},
            {'Indicador':'Primer contacto','Total':primer_contacto},
            {'Indicador':'Total','Total':total},]

#### Callback for mes table
@app.callback(Output('mes-table-registros', 'data'),
	[Input('my-date-picker-range-registros', 'start_date'),
	 Input('my-date-picker-range-registros', 'end_date'),
     Input('dropdown-distritos-registros', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df_1 = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df_1 = filtered_df_1.drop_duplicates(subset="VISITORID").reset_index()
    filtered_df_1 = filtered_df_1[filtered_df_1["PAIS"]=='COLOMBIA'].reset_index(drop=True)
    filtered_df_1 = filtered_df_1[filtered_df_1["DISTRITO"].isin(distritos)]
    filtered_df_1 = filtered_df_1.groupby(by=["YEAR","MONTH"]).agg({'VISITORID':'count'}).reset_index()
    filtered_df_1['MONTH'] = filtered_df_1['MONTH'].map(string_months)

    filtered_df_2 = df_primer[df_primer.FECHA_PRIMER_CONTACTO.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df_2 = filtered_df_2.drop_duplicates(subset="ID").reset_index()
    filtered_df_2 = filtered_df_2[filtered_df_2["DISTRITO"].isin(distritos)]
    filtered_df_2 = filtered_df_2.groupby(by=["YEAR","MONTH"]).agg({'ID':'nunique'}).reset_index()
    filtered_df_2['MONTH'] = filtered_df_2['MONTH'].map(string_months)

    filtered_df = pd.merge(left=filtered_df_1,right=filtered_df_2,on=['YEAR','MONTH'],how='left')
    filtered_df['VISITORID'] = filtered_df['VISITORID'].fillna(0)
    filtered_df['ID'] = filtered_df['ID'].fillna(0)
    filtered_df['TOT'] = filtered_df['VISITORID']+filtered_df['ID']

    filtered_df.columns = ["Año","Mes","Registros Nuevos","Primer Contacto","Total"]
    data_mes = filtered_df.to_dict("rows")
    return data_mes

#### Callback for dia table
@app.callback(Output('dia-table-registros', 'data'),
	[Input('my-date-picker-range-registros', 'start_date'),
	 Input('my-date-picker-range-registros', 'end_date'),
     Input('dropdown-distritos-registros', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df_1 = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df_1 = filtered_df_1[filtered_df_1["DISTRITO"].isin(distritos)]
    filtered_df_1 = filtered_df_1.drop_duplicates(subset="VISITORID").reset_index()
    filtered_df_1 = filtered_df_1[filtered_df_1["PAIS"]=='COLOMBIA'].reset_index(drop=True)
    filtered_df_1 = filtered_df_1[filtered_df_1["DISTRITO"].isin(distritos)]

    filtered_df_2 = df_primer[df_primer.FECHA_PRIMER_CONTACTO.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df_2 = filtered_df_2.drop_duplicates(subset="ID").reset_index()
    filtered_df_2 = filtered_df_2[filtered_df_2["DISTRITO"].isin(distritos)]

    if distritos==[]:
        month = 0
        year = 0
    else:
        month = int(filtered_df_1.DATE.max().month)
        year = int(filtered_df_1.DATE.max().year)

    filtered_df_1 = filtered_df_1[(filtered_df_1["MONTH"]==month)&(filtered_df_1["YEAR"]==year)]
    filtered_df_1["MONTH"] = filtered_df_1["MONTH"].map(string_months)
    filtered_df_1 = filtered_df_1.groupby(by=["YEAR","MONTH","DAY"]).agg({'VISITORID':'nunique'}).reset_index()
    filtered_df_1["DAY"] = filtered_df_1["MONTH"] + "-" + filtered_df_1["DAY"].astype(str)

    filtered_df_2 = filtered_df_2[(filtered_df_2["MONTH"]==month)&(filtered_df_2["YEAR"]==year)]
    filtered_df_2["MONTH"] = filtered_df_2["MONTH"].map(string_months)
    filtered_df_2 = filtered_df_2.groupby(by=["YEAR","MONTH","DAY"]).agg({'ID':'nunique'}).reset_index()
    filtered_df_2["DAY"] = filtered_df_2["MONTH"] + "-" + filtered_df_2["DAY"].astype(str)

    filtered_df = pd.merge(left=filtered_df_1,right=filtered_df_2,on=['YEAR','MONTH','DAY'],how='left')
    filtered_df['VISITORID'] = filtered_df['VISITORID'].fillna(0)
    filtered_df['ID'] = filtered_df['ID'].fillna(0)
    filtered_df['TOT'] = filtered_df['VISITORID']+filtered_df['ID']

    filtered_df = filtered_df[['YEAR','DAY','VISITORID','ID','TOT']]
    filtered_df.columns = ['Año','Dia','REGISTROS','PRIMER','TOT']

    data_dia = filtered_df.to_dict("rows")
    return data_dia

#### Update graph registros por distritos
@app.callback(
    Output('registros-distritos', 'figure'),
    [Input('my-date-picker-range-registros', 'start_date'),
     Input('my-date-picker-range-registros', 'end_date'),
     Input('dropdown-distritos-registros', 'value')])
def update_graph_TipoPro_total(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    filtered_df = filtered_df.groupby(by='DISTRITO').agg({'VISITORID':'nunique'}).reset_index()
    trace = go.Pie(
                    values  = filtered_df['VISITORID'].tolist(),
                    labels  = filtered_df['DISTRITO'].tolist(),
                    hoverinfo = "label+percent+value",
                    marker  = dict(line = dict(width = 2,
                                               color = "rgb(243,243,243)")
                                  ),
                    text= filtered_df['VISITORID'].tolist(),
                    domain  = dict(x = [0,1]),
                    hole    = .5,
                    marker_colors=colors,
                )
    layout = go.Layout(dict(
                    title = "",
                    legend_bgcolor = "rgb(255,255,255)",
                    plot_bgcolor  = "rgb(255,255,255)",
                    paper_bgcolor = "rgb(255,255,255)",
                    margin=dict(t=50),
                    annotations = [dict(text = "Distrito",
                                        font = dict(size = 13),
                                        showarrow = False,
                                        x = .5, y = .5),],
                                           )
                )
    return {
        "data": [trace],
        "layout": layout
    }

#### Callback for distrito-Ciudad table
@app.callback(Output('ciudad-table-registros', 'data'),
	[Input('my-date-picker-range-registros', 'start_date'),
	 Input('my-date-picker-range-registros', 'end_date'),
     Input('dropdown-distritos-registros', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    data_distrito = filtered_df.groupby(by=['DISTRITO','CIUDAD']).agg({'VISITORID':'nunique'}).reset_index()
    data_distrito = data_distrito.sort_values(by='VISITORID',ascending=False).reset_index(drop=True)
    data_distrito['DISTRITO'] = data_distrito['DISTRITO'].apply(lambda x: x.capitalize())
    data_distrito['CIUDAD'] = data_distrito['CIUDAD'].apply(lambda x: x.capitalize())
    total_registros = data_distrito['VISITORID'].sum()
    data_distrito['% Total Registros'] = (data_distrito['VISITORID']*100/total_registros).round(decimals=2)
    data_distrito = data_distrito.to_dict("rows")
    return data_distrito

#### Update graph registros por etapa
@app.callback(
    Output('registros-edad', 'figure'),
    [Input('my-date-picker-range-registros', 'start_date'),
     Input('my-date-picker-range-registros', 'end_date'),
     Input('dropdown-distritos-registros', 'value')])
def update_graph_TipoPro_total(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    filtered_df = filtered_df.groupby(by='ETAPA_BEBE').agg({'VISITORID':'count'}).reset_index()
    filtered_df = filtered_df.sort_values(by='VISITORID', ascending=False)
    total_inscritos = filtered_df.VISITORID.sum()
    filtered_df['PROP'] =  (filtered_df['VISITORID']*100/total_inscritos).round(decimals=1)
    filtered_df['TEXT'] =  filtered_df['PROP'].astype(str) + '%'
    trace = go.Bar(
                x = filtered_df['ETAPA_BEBE'],
                y = filtered_df['VISITORID'],
                text = filtered_df['TEXT'],
                textposition='auto',
            )
    layout = go.Layout(dict(
                            title = "",
                            legend_bgcolor = "rgb(255,255,255)",
                            plot_bgcolor  = "rgb(255,255,255)",
                            paper_bgcolor = "rgb(255,255,255)",
                            margin=dict(t=50),
                        )
                )
    return {
        "data": [trace],
        "layout": layout
    }

#### Update graph registros por medio
@app.callback(
    Output('registros-medio', 'figure'),
    [Input('my-date-picker-range-registros', 'start_date'),
     Input('my-date-picker-range-registros', 'end_date'),
     Input('dropdown-distritos-registros', 'value')])
def update_graph_TipoPro_total(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_registros[df_registros.FECHA_INSCRIPCION.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    filtered_df['MEDIO'] = filtered_df['MEDIO_INSCRIPCION'].map(dir_medio_insc)
    filtered_df = filtered_df.groupby(by='MEDIO').agg({'VISITORID':'nunique'}).reset_index()
    trace = go.Pie(
                    values  = filtered_df['VISITORID'].tolist(),
                    labels  = filtered_df['MEDIO'].tolist(),
                    hoverinfo = "label+percent+value",
                    marker  = dict(line = dict(width = 2,
                                               color = "rgb(243,243,243)")
                                  ),
                    text= filtered_df['VISITORID'].tolist(),
                    domain  = dict(x = [0,1]),
                    hole    = .5,
                    marker_colors=colors,
                )
    layout = go.Layout(dict(
                    title = "",
                    legend_bgcolor = "rgb(255,255,255)",
                    plot_bgcolor  = "rgb(255,255,255)",
                    paper_bgcolor = "rgb(255,255,255)",
                    margin=dict(t=50),
                    annotations = [dict(text = "Medio de Inscripción",
                                        font = dict(size = 13),
                                        showarrow = False,
                                        x = .5, y = .5),],
                                           )
                )
    return {
        "data": [trace],
        "layout": layout
    }

#### Callback for total table activos
@app.callback(Output('table-total-activos', 'data'),
	[Input('dropdown-distritos-registros', 'value')])
def update_data_1(distritos):
    filtered_df = df_activas[df_activas["DISTRITO"].isin(distritos)].reset_index(drop=True)
    total = filtered_df.USUARIAS.sum()
    oro = filtered_df[filtered_df.SEGMENTO=='Oro'].USUARIAS.sum()
    plata = filtered_df[filtered_df.SEGMENTO=='Plata'].USUARIAS.sum()
    bronce = filtered_df[filtered_df.SEGMENTO=='Bronce'].USUARIAS.sum()
    return [{'Segmento':'Total activos','Número de Usuarios':total},
            {'Segmento':'Oro','Número de Usuarios':oro},
            {'Segmento':'Plata','Número de Usuarios':plata},
            {'Segmento':'Bronce','Número de Usuarios':bronce},]


#### Update graph activos por  etapa
@app.callback(
    Output('activos-etapa', 'figure'),
    [Input('dropdown-distritos-registros', 'value')])
def update_graph_TipoPro_total(distritos):
    dir_etapa = {'embarazada':0,'recien nacido': 1, 'acostadito':2, 'explorador':3, 'aventurero':4,'36 o mayor':5}
    filtered_df = df_activas[df_activas["DISTRITO"].isin(distritos)]
    filtered_df = filtered_df.groupby(by=['ETAPA_BEBE']).agg({'USUARIAS':'sum'}).reset_index()
    filtered_df['etapa_orden'] =  filtered_df['ETAPA_BEBE'].map(dir_etapa)
    filtered_df.sort_values(by='etapa_orden',inplace=True)
    total_act =  filtered_df.USUARIAS.sum()
    filtered_df['text'] = filtered_df['USUARIAS'].astype(str) + ' - ' +(filtered_df['USUARIAS']*100/total_act).round(1).astype(str)+'%'

    trace = go.Bar(
                        x = filtered_df.ETAPA_BEBE,
                        y = filtered_df.USUARIAS,
                        text = filtered_df.text,
                        textposition='auto',
                        name = '',
                        marker_color='#4179bd'
                    )

    data = [trace]

    layout = go.Layout(dict(title = "",
                        legend_bgcolor = "rgb(255,255,255)",
                        plot_bgcolor  = "rgb(255,255,255)",
                        paper_bgcolor = "rgb(255,255,255)",
                        barmode='group',
                        margin=dict(t=50),
                     )
                  )

    return {
        "data": data,
        "layout": layout
    }


#### Update graph activos por distritos
@app.callback(
    Output('activos-distrito', 'figure'),
    [Input('dropdown-distritos-registros', 'value')])
def update_graph_TipoPro_total(distritos):
    filtered_df = df_activas[df_activas["DISTRITO"].isin(distritos)]
    filtered_df = filtered_df.groupby(by='DISTRITO').agg({'USUARIAS':'sum'}).reset_index()
    trace = go.Pie(
                    values  = filtered_df['USUARIAS'].tolist(),
                    labels  = filtered_df['DISTRITO'].tolist(),
                    hoverinfo = "label+percent+value",
                    marker  = dict(line = dict(width = 2,
                                               color = "rgb(243,243,243)")
                                  ),
                    text= filtered_df['USUARIAS'].tolist(),
                    domain  = dict(x = [0,1]),
                    hole    = .5,
                    marker_colors=colors,
                )
    layout = go.Layout(dict(
                    title = "",
                    legend_bgcolor = "rgb(255,255,255)",
                    plot_bgcolor  = "rgb(255,255,255)",
                    paper_bgcolor = "rgb(255,255,255)",
                    margin=dict(t=50),
                    annotations = [dict(text = "Distrito",
                                        font = dict(size = 13),
                                        showarrow = False,
                                        x = .5, y = .5),],
                                           )
                )
    return {
        "data": [trace],
        "layout": layout
    }

#### Callback for Activos por distrito-Ciudad table
@app.callback(Output('ciudad-table-activos', 'data'),
	[Input('dropdown-distritos-registros', 'value')])
def update_data_activos(distritos):
    filtered_df = df_activas[df_activas["DISTRITO"].isin(distritos)].reset_index(drop=True)
    data_distrito = filtered_df.groupby(by=['DISTRITO','CIUDAD']).agg({'USUARIAS':'sum'}).reset_index()
    data_distrito = data_distrito.sort_values(by='USUARIAS',ascending=False).reset_index(drop=True)
    data_distrito['DISTRITO'] = data_distrito['DISTRITO'].apply(lambda x: x.capitalize())
    data_distrito['CIUDAD'] = data_distrito['CIUDAD'].apply(lambda x: x.capitalize())
    total_registros = data_distrito['USUARIAS'].sum()
    data_distrito['% Total Activos'] = (data_distrito['USUARIAS']*100/total_registros).round(decimals=2)
    data_distrito = data_distrito.to_dict("rows")
    return data_distrito


#### Callback for mes table Activos

######################## END Análitico de REGISTROS Callbacks #######################


######################## Start Análitico de CLAVES Callbacks ########################

#### Date Dropdown Distritos
@app.callback(Output('dropdown-distritos-claves', 'value'),
	[Input('items-options-distrito-claves', 'value')])
def update_dropdown_distritos(option):
    if option == 'TODOS':
        return ['CUNDI-BOY','ANTIOQUIA','CENTRO','PACIFICO', 'OTROS', 'ATLANTICO', 'SANTANDERES', 'EJE CAFETERO',
                'LLANOS','OTRO']
    else:
        return []

#### Date Picker Callback
@app.callback(Output('output-container-date-picker-claves', 'children'),
	[Input('my-date-picker-range-claves', 'start_date'),
	 Input('my-date-picker-range-claves', 'end_date')])
def update_output(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    number_days = (end_date - start_date).days
    return 'Se seleccionaron '+str(number_days)+' días'

#### Update graph mensual Callback
@app.callback(
    Output('claves-mes', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun', 'value'),
     Input('dropdown-distritos-claves', 'value')])
def update_graph_mes(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    filtered_df = filtered_df.groupby(by=['YEAR','MONTH'])[column].sum().reset_index()
    filtered_df['MONTH'] = filtered_df['MONTH'].map(string_months)
    return update_graph_scatter(df=filtered_df,column=column,per="MONTH")

#### Update graph diaria Callback
@app.callback(
    Output('claves-dia', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun', 'value'),
     Input('dropdown-distritos-claves', 'value')])
def update_graph_dia(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    if distritos==[]:
        month = 0
    else:
        month = int(filtered_df.DATE.max().month)
    filtered_df = filtered_df[filtered_df["MONTH"].astype(int)==month].reset_index(drop=True)
    filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
    filtered_df = filtered_df.groupby(by=["YEAR","MONTH","DAY"])[column].sum().reset_index()
    filtered_df["DAY"] = filtered_df["MONTH"] + "-" + filtered_df["DAY"].astype(str)
    return update_graph_scatter(df=filtered_df,column=column,per="DAY")

#### Callback for total table
@app.callback(Output('total-table-claves', 'data'),
	[Input('my-date-picker-range-claves', 'start_date'),
	 Input('my-date-picker-range-claves', 'end_date'),
     Input('dropdown-distritos-claves', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    data_total = filtered_df[["CLAVES","PUNTOS"]].sum().reset_index()
    data_total.columns = ["Indicador","Total"]
    data_total = data_total.to_dict("rows")
    return data_total

#### Callback for mes table
@app.callback(Output('mes-table-claves', 'data'),
	[Input('my-date-picker-range-claves', 'start_date'),
	 Input('my-date-picker-range-claves', 'end_date'),
     Input('dropdown-distritos-claves', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    data_mes = filtered_df.groupby(by=['YEAR','MONTH'])["CLAVES","PUNTOS"].sum().reset_index()
    data_mes = data_mes.sort_values(by=["YEAR","MONTH"], ascending=False).reset_index(drop=True)
    data_mes["MONTH"] = data_mes["MONTH"].map(string_months)
    data_mes.columns = ["Año","Mes","Claves","Puntos"]
    data_mes = data_mes.to_dict("rows")
    return data_mes

#### Callback for dia table
@app.callback(Output('dia-table-claves', 'data'),
	[Input('my-date-picker-range-claves', 'start_date'),
	 Input('my-date-picker-range-claves', 'end_date'),
     Input('dropdown-distritos-claves', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    if distritos==[]:
        month = 0
        year = 0
    else:
        month = int(filtered_df.DATE.max().month)
        year = int(filtered_df.DATE.max().year)
    data_dia = filtered_df[(filtered_df["MONTH"]==month)&(filtered_df["YEAR"]==year)]
    data_dia = data_dia.groupby(by=["YEAR","MONTH","DAY"])["CLAVES","PUNTOS"].sum().reset_index()
    data_dia = data_dia.sort_values(by="DAY",ascending=False)
    data_dia["MONTH"] = data_dia["MONTH"].map(string_months)
    data_dia["DAY"] = data_dia["MONTH"] + "-" + data_dia["DAY"].astype(str)
    data_dia = data_dia[["YEAR","DAY","CLAVES","PUNTOS"]].reset_index(drop=True)
    data_dia.columns = ["Año","Día","Claves","Puntos"]
    data_dia = data_dia.to_dict("rows")
    return data_dia

#### Update graph distritos Callback
@app.callback(
    Output('claves-distrito', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun-distrito', 'value'),
     Input('dropdown-distritos-claves', 'value')])
def update_graph_distrito(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    return update_graph_pie(df=filtered_df,column=column)

#### Callback for distrito table
@app.callback(Output('distrito-table-claves', 'data'),
	[Input('my-date-picker-range-claves', 'start_date'),
	 Input('my-date-picker-range-claves', 'end_date'),
     Input('dropdown-distritos-claves', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    data_distrito = filtered_df.groupby(by=['DISTRITO','CIUDAD'])['CLAVES','PUNTOS'].sum().reset_index()
    data_distrito = data_distrito.sort_values(by='CLAVES',ascending=False).reset_index(drop=True)
    total_claves = data_distrito['CLAVES'].sum()
    total_puntos = data_distrito['PUNTOS'].sum()
    data_distrito['DISTRITO'] = data_distrito['DISTRITO'].apply(lambda x: x.capitalize())
    data_distrito['CIUDAD'] = data_distrito['CIUDAD'].apply(lambda x: x.capitalize())
    data_distrito['% Total Claves'] = (data_distrito['CLAVES']*100/total_claves).round(decimals=2)
    data_distrito['% Total Puntos'] = (data_distrito['PUNTOS']*100/total_puntos).round(decimals=2)
    data_distrito = data_distrito[['DISTRITO','CIUDAD','CLAVES','% Total Claves','PUNTOS','% Total Puntos']]
    data_distrito = data_distrito.to_dict("rows")
    return data_distrito

#### Update graph por tipo (total) Callback
@app.callback(
    Output('claves-tipo-total', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun-TipoPro', 'value'),
     Input('dropdown-distritos-claves', 'value')])
def update_graph_TipoPro_total(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    df_clasificacion_claves
    filtered_df = filtered_df.groupby(by=['CATEGORIAS','SEGMENTO','SUBSEGMENTO']).agg({'CLAVES':'sum','PUNTOS':'sum'}).reset_index()
    filtered_df = pd.merge(left=filtered_df,right=df_clasificacion_claves,on=['CATEGORIAS','SEGMENTO','SUBSEGMENTO'],how='left')
    filtered_df['CATEGORIAS'] = filtered_df['CATEGORIAS'].str.replace('?','Ñ')
    df_clav_tipo_pro = filtered_df.groupby(by='Clasificacion').agg({'CLAVES':'sum','PUNTOS':'sum'}).reset_index()
    trace = go.Pie(
                    values  = df_clav_tipo_pro[column].tolist(),
                    labels  = df_clav_tipo_pro['Clasificacion'].tolist(),
                    hoverinfo = "label+percent+value",
                    marker  = dict(line = dict(width = 2,
                                               color = "rgb(243,243,243)")
                                  ),
                    #text= df_clav_tipo_pro[column].tolist(),
                    domain  = dict(x = [0,1]),
                    hole    = .5,
                    marker_colors=colors,
                )
    layout = go.Layout(dict(
                    title = "",
                    legend_bgcolor = "rgb(255,255,255)",
                    plot_bgcolor  = "rgb(255,255,255)",
                    paper_bgcolor = "rgb(255,255,255)",
                    margin=dict(t=50),
                    annotations = [dict(text = "Categoría Producto",
                                        font = dict(size = 13),
                                        showarrow = False,
                                        x = .5, y = .5),],
                                           )
                )
    return {
        "data": [trace],
        "layout": layout
    }

#### Update graph por tipo (diário) Callback
@app.callback(
    Output('claves-tipo-dia', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun-TipoPro', 'value'),
     Input('dropdown-distritos-claves', 'value')])
def update_graph_TipoPro_dia(start_date, end_date, column, distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    if distritos==[]:
        month = 0
        year = 0
    else:
        month = int(filtered_df.DATE.max().month)
        year = int(filtered_df.DATE.max().year)

    filtered_df = filtered_df[(filtered_df["MONTH"]==month)&(filtered_df["YEAR"]==year)]
    filtered_df = filtered_df.groupby(by=["MONTH","DAY","CATEGORIAS","SEGMENTO","SUBSEGMENTO"])[column].sum().reset_index()
    filtered_df = pd.merge(left=filtered_df,right=df_clasificacion_claves,on=['CATEGORIAS','SEGMENTO','SUBSEGMENTO'],how='left')
    filtered_df = filtered_df.groupby(by=["MONTH","DAY","Clasificacion"])[column].sum().reset_index()
    filtered_df = filtered_df.sort_values(by="DAY")
    filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
    title = list(filtered_df["MONTH"])[0]
    filtered_df = filtered_df[["DAY","Clasificacion",column]].reset_index(drop=True)
    categorias = list(set(filtered_df["Clasificacion"]))
    n = len(categorias)
    data = []
    x = filtered_df['DAY'].unique().tolist()
    for i in range(n):
        trace = go.Bar(
                            x = x,
                            y = filtered_df[filtered_df["Clasificacion"]==categorias[i]][column],
                            name = str(categorias[i]),
                            marker_color=colors[i]
                        )
        data.append(trace)

    layout = go.Layout(dict(title = title,
                        legend_bgcolor = "rgb(255,255,255)",
                        plot_bgcolor  = "rgb(255,255,255)",
                        paper_bgcolor = "rgb(255,255,255)",
                        showlegend=True,
                        margin=dict(t=50),
                        barmode='stack'
                     )
                  )

    return {
        "data": data,
        "layout": layout
    }

#### Callback for cat-seg-subseg table
@app.callback(Output('cat_seg_subseg-table-claves', 'data'),
	[Input('my-date-picker-range-claves', 'start_date'),
	 Input('my-date-picker-range-claves', 'end_date'),
     Input('dropdown-distritos-claves', 'value')])
def update_data_1(start_date, end_date,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    filtered_df = filtered_df.groupby(by=['CATEGORIAS','SEGMENTO','SUBSEGMENTO']).agg({'CLAVES':'sum','PUNTOS':'sum'}).reset_index()
    total_claves = filtered_df['CLAVES'].sum()
    total_puntos = filtered_df['PUNTOS'].sum()
    filtered_df['% Total Claves'] = (filtered_df['CLAVES']*100/total_claves).round(decimals=2)
    filtered_df['% Total Puntos'] = (filtered_df['PUNTOS']*100/total_puntos).round(decimals=2)
    filtered_df = pd.merge(left=filtered_df,right=df_clasificacion_claves,on=['CATEGORIAS','SEGMENTO','SUBSEGMENTO'],how='left')
    filtered_df['Clasificacion'] = filtered_df['Clasificacion'].apply(lambda x: x.capitalize())
    filtered_df['SEGMENTO'] = filtered_df['SEGMENTO'].apply(lambda x: x.capitalize())
    filtered_df['SUBSEGMENTO'] = filtered_df['SUBSEGMENTO'].apply(lambda x: x.capitalize())
    filtered_df = filtered_df[['Clasificacion','SEGMENTO','SUBSEGMENTO','CLAVES','% Total Claves','PUNTOS','% Total Puntos']]
    data_cat_seg_subseg = filtered_df.to_dict("rows")
    return data_cat_seg_subseg

#### Update graph por medio  Callback
@app.callback(
    Output('claves-medio', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun-medio', 'value'),
     Input('dropdown-distritos-claves', 'value')])
def update_graph_TipoPro_dia(start_date, end_date, column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_med[df_claves_med.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    filtered_df = filtered_df.groupby(by=["YEAR","MONTH","MEDIOS_INGRESO"])[column].sum().reset_index()
    filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
    filtered_df["YEAR_MONTH"] = filtered_df["YEAR"].astype(str) + "-" + filtered_df["MONTH"].astype(str)
    filtered_df = filtered_df[["YEAR_MONTH","MEDIOS_INGRESO",column]].reset_index(drop=True)
    medios = list(set(filtered_df["MEDIOS_INGRESO"]))
    n = len(medios)
    data = []
    x = filtered_df['YEAR_MONTH'].unique().tolist()
    for i in range(n):
        trace = go.Bar(
                            x = x,
                            y = filtered_df[filtered_df["MEDIOS_INGRESO"]==medios[i]][column],
                            name = str(medios[i]),
                            marker_color=colors[i],
                        )
        data.append(trace)

    layout = go.Layout(dict(title = "",
                        legend_bgcolor = "rgb(255,255,255)",
                        plot_bgcolor  = "rgb(255,255,255)",
                        paper_bgcolor = "rgb(255,255,255)",
                        showlegend=True,
                        barmode='stack',
                        margin=dict(t=50)
                        )
                     )


    return {
        "data": data,
        "layout": layout
    }
######################## END Análitico de CLAVES Callbacks ########################




##########################################################################################
######################## START Análitico de Redenciones Callbacks ########################
#### Date Dropdown Distritos
@app.callback(Output('dropdown-distritos-redenciones', 'value'),
	[Input('items-options-distrito-redenciones', 'value')])
def update_dropdown_distritos(option):
    if option == 'TODOS':
        return ['CUNDI-BOY','ANTIOQUIA','CENTRO','PACIFICO', 'OTROS', 'ATLANTICO', 'SANTANDERES', 'EJE CAFETERO',
                'LLANOS','OTRO']
    else:
        return []

#### Date Picker Callback
@app.callback(Output('output-container-date-picker-redenciones', 'children'),
	[Input('my-date-picker-range-redenciones', 'start_date'),
	 Input('my-date-picker-range-redenciones', 'end_date')])
def update_output(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    number_days = (end_date - start_date).days
    return 'Se seleccionaron '+str(number_days)+' días'

#### Red Puntos Item options Callback
@app.callback([Output('items-options-redt_redf_redv', 'options'),
    Output('items-options-redt_redf_redv', 'value')],
	[Input('items-options-red_puntos', 'value')])
def update_output(RED_PUNTOS):
    if RED_PUNTOS == 'RED':
        options = [
            {'label': 'Totales', 'value': 'RED_TOT'},
            {'label': 'Físicas', 'value': 'RED_FIS'},
            {'label': 'Virtuales', 'value': 'RED_VIR'},
            {'label': 'Regalos', 'value': 'RED_REG'},
        ]
        value = 'RED_TOT'
    else:
        options = [
            {'label': 'Totales', 'value': 'PUNTOS_TOT'},
            {'label': 'Físicas', 'value': 'PUNTOS_FIS'},
            {'label': 'Virtuales', 'value': 'PUNTOS_VIR'},
            {'label': 'Regalos', 'value': 'PUNTOS_REG'},
        ]
        value = 'PUNTOS_TOT'

    return options, value

#### Update graph mensual Callback
@app.callback(
    Output('redenciones-mes', 'figure'),
    [Input('my-date-picker-range-redenciones', 'start_date'),
     Input('my-date-picker-range-redenciones', 'end_date'),
     Input('items-options-redt_redf_redv', 'value'),
     Input('dropdown-distritos-redenciones', 'value')])
def update_graph_mes(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    filtered_df = filtered_df.groupby(by=['YEAR','MONTH'])[column].sum().reset_index()
    filtered_df['MONTH'] = filtered_df['MONTH'].map(string_months)
    return update_graph_scatter(df=filtered_df,column=column,per="MONTH")

#### Update graph diaria Callback
@app.callback(
    Output('redenciones-dia', 'figure'),
    [Input('my-date-picker-range-redenciones', 'start_date'),
     Input('my-date-picker-range-redenciones', 'end_date'),
     Input('items-options-redt_redf_redv', 'value'),
     Input('dropdown-distritos-redenciones', 'value')])
def update_graph_dia(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    if distritos==[]:
        month = 0
    else:
        month = int(filtered_df.DATE.max().month)
    filtered_df = filtered_df[filtered_df["MONTH"].astype(int)==month].reset_index(drop=True)
    filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
    filtered_df = filtered_df.groupby(by=["YEAR","MONTH","DAY"])[column].sum().reset_index()
    filtered_df["DAY"] = filtered_df["MONTH"] + "-" + filtered_df["DAY"].astype(str)
    return update_graph_scatter(df=filtered_df,column=column,per="DAY")


#### Callback for total table
@app.callback(Output('total-table-redenciones', 'data'),
	[Input('my-date-picker-range-redenciones', 'start_date'),
	 Input('my-date-picker-range-redenciones', 'end_date'),
     Input('dropdown-distritos-redenciones', 'value'),
     Input('items-options-redt_redf_redv-tabla', 'value')])
def update_data_1(start_date, end_date,distritos,tot_fis_vir_reg):
    RED = "RED_"+tot_fis_vir_reg
    PUNTOS = "PUNTOS_"+tot_fis_vir_reg
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    data_total = filtered_df[[RED,PUNTOS]].sum().reset_index()
    data_total.columns = ["Indicador","Total"]
    data_total = data_total.to_dict("rows")
    return data_total

#### Callback for mes table
@app.callback(Output('mes-table-redenciones', 'data'),
	[Input('my-date-picker-range-redenciones', 'start_date'),
	 Input('my-date-picker-range-redenciones', 'end_date'),
     Input('dropdown-distritos-redenciones', 'value'),
     Input('items-options-redt_redf_redv-tabla', 'value')])
def update_data_1(start_date, end_date,distritos,tot_fis_vir_reg):
    RED = "RED_"+tot_fis_vir_reg
    PUNTOS = "PUNTOS_"+tot_fis_vir_reg
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    data_mes = filtered_df.groupby(by=['YEAR','MONTH']).agg({RED:sum, PUNTOS:sum}).reset_index()
    data_mes = data_mes.sort_values(by=["YEAR","MONTH"], ascending=False).reset_index(drop=True)
    data_mes["MONTH"] = data_mes["MONTH"].map(string_months)
    data_mes.columns = ["Año","Mes","Redenciones","Puntos"]
    data_mes = data_mes.to_dict("rows")
    return data_mes

#### Callback for dia table
@app.callback(Output('dia-table-redenciones', 'data'),
	[Input('my-date-picker-range-redenciones', 'start_date'),
	 Input('my-date-picker-range-redenciones', 'end_date'),
     Input('dropdown-distritos-redenciones', 'value'),
     Input('items-options-redt_redf_redv-tabla', 'value')])
def update_data_1(start_date, end_date,distritos,tot_fis_vir_reg):
    RED = "RED_"+tot_fis_vir_reg
    PUNTOS = "PUNTOS_"+tot_fis_vir_reg
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    if distritos==[]:
        month = 0
        year = 0
    else:
        month = int(filtered_df.DATE.max().month)
        year = int(filtered_df.DATE.max().year)
    data_dia = filtered_df[(filtered_df["MONTH"]==month)&(filtered_df["YEAR"]==year)]
    data_dia = data_dia.groupby(by=["YEAR","MONTH","DAY"]).agg({RED:sum, PUNTOS:sum}).reset_index()
    data_dia = data_dia.sort_values(by="DAY",ascending=False)
    data_dia["MONTH"] = data_dia["MONTH"].map(string_months)
    data_dia["DAY"] = data_dia["MONTH"] + "-" + data_dia["DAY"].astype(str)
    data_dia = data_dia[["YEAR","DAY",RED,PUNTOS]].reset_index(drop=True)
    data_dia.columns = ["Año","Día","Redenciones","Puntos"]
    data_dia = data_dia.to_dict("rows")
    return data_dia

#### Red Puntos Item options Callback
@app.callback([Output('items-options-redt_redf_redv-dist', 'options'),
    Output('items-options-redt_redf_redv-dist', 'value')],
	[Input('items-options-red_puntos-dist', 'value')])
def update_output(RED_PUNTOS):
    if RED_PUNTOS == 'RED':
        options = [
            {'label': 'Totales', 'value': 'RED_TOT'},
            {'label': 'Físicas', 'value': 'RED_FIS'},
            {'label': 'Virtuales', 'value': 'RED_VIR'},
            {'label': 'Regalos', 'value': 'RED_REG'},
        ]
        value = 'RED_TOT'
    else:
        options = [
            {'label': 'Totales', 'value': 'PUNTOS_TOT'},
            {'label': 'Físicas', 'value': 'PUNTOS_FIS'},
            {'label': 'Virtuales', 'value': 'PUNTOS_VIR'},
            {'label': 'Regalos', 'value': 'PUNTOS_REG'},
        ]
        value = 'PUNTOS_TOT'

    return options, value

#### Update graph distritos Callback
@app.callback(
    Output('redenciones-distrito', 'figure'),
    [Input('my-date-picker-range-redenciones', 'start_date'),
     Input('my-date-picker-range-redenciones', 'end_date'),
     Input('items-options-redt_redf_redv-dist', 'value'),
     Input('dropdown-distritos-redenciones', 'value')])
def update_graph_distrito(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)]
    return update_graph_pie(df=filtered_df,column=column)

#### Callback for distrito table
@app.callback(Output('distrito-table-redenciones', 'data'),
	[Input('my-date-picker-range-redenciones', 'start_date'),
	 Input('my-date-picker-range-redenciones', 'end_date'),
     Input('dropdown-distritos-redenciones', 'value'),
     Input('items-options-redt_redf_redv-tabla-dist', 'value')])
def update_data_1(start_date, end_date,distritos,tot_fis_vir_reg):
    RED = "RED_"+tot_fis_vir_reg
    PUNTOS = "PUNTOS_"+tot_fis_vir_reg
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    data_distrito = filtered_df.groupby(by=['DISTRITO','CIUDAD']).agg({RED:sum, PUNTOS:sum}).reset_index()
    data_distrito = data_distrito.sort_values(by=RED,ascending=False).reset_index(drop=True)
    total_red = data_distrito[RED].sum()
    total_puntos = data_distrito[PUNTOS].sum()
    data_distrito['DISTRITO'] = data_distrito['DISTRITO'].apply(lambda x: x.capitalize())
    data_distrito['CIUDAD'] = data_distrito['CIUDAD'].apply(lambda x: x.capitalize())
    data_distrito['% Total Redenciones'] = (data_distrito[RED]*100/total_red).round(decimals=2)
    data_distrito['% Total Puntos'] = (data_distrito[PUNTOS]*100/total_puntos).round(decimals=2)
    data_distrito = data_distrito[['DISTRITO','CIUDAD',RED,'% Total Redenciones',PUNTOS,'% Total Puntos']]
    data_distrito.columns = ['DISTRITO','CIUDAD','RED','% Total Redenciones','PUNTOS','% Total Puntos']
    data_distrito = data_distrito.to_dict("rows")
    return data_distrito

#### Callback for distrito table
@app.callback(Output('punto_red-table-redenciones', 'data'),
	[Input('my-date-picker-range-redenciones', 'start_date'),
	 Input('my-date-picker-range-redenciones', 'end_date'),
     Input('dropdown-distritos-redenciones', 'value'),
     Input('items-options-redt_redf_redv-tabla-punto_red', 'value')])
def update_data_1(start_date, end_date,distritos,tot_fis_vir_reg):
    RED = "RED_"+tot_fis_vir_reg
    PUNTOS = "PUNTOS_"+tot_fis_vir_reg
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_red_lug[df_red_lug.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    data_medio = filtered_df.groupby(by=['LUGAR_COMPRA']).agg({RED:sum, PUNTOS:sum}).reset_index()
    data_medio = data_medio.sort_values(by=RED,ascending=False).reset_index(drop=True)
    total_red = data_medio[RED].sum()
    total_puntos = data_medio[PUNTOS].sum()
    data_medio['LUGAR_COMPRA'] = data_medio['LUGAR_COMPRA'].apply(lambda x: x.capitalize())
    data_medio['LUGAR_COMPRA'] = data_medio['LUGAR_COMPRA'].str.replace('?','ñ')
    data_medio['% Total Redenciones'] = (data_medio[RED]*100/total_red).round(decimals=2)
    data_medio['% Total Puntos'] = (data_medio[PUNTOS]*100/total_puntos).round(decimals=2)
    data_medio = data_medio[['LUGAR_COMPRA',RED,'% Total Redenciones',PUNTOS,'% Total Puntos']]
    data_medio.columns = ['LUGAR_COMPRA','RED','% Total Redenciones','PUNTOS','% Total Puntos']
    data_medio = data_medio.to_dict("rows")
    return data_medio

######################## END Análitico de Redenciones Callbacks ########################
########################################################################################

#####################################################################################
######################## START Análitico de Portal Callbacks ########################


######################## END Análitico de Portal Callbacks ########################
###################################################################################

#### Update graph mensual Callback
@app.callback(
    Output('portal-mes', 'figure'),
    [Input('dropdown-portal-opciones-mes', 'value')])
def update_graph_mensual(column):
    filtered_df = df_portal_mensual.copy()
    filtered_df['YEAR'] = filtered_df['Month'].apply(lambda x: x.split('-')[0])
    filtered_df['MONTH'] = filtered_df['Month'].apply(lambda x: x.split('-')[1])
    filtered_df['MONTH'] = filtered_df['MONTH'].astype(int).map(string_months)
    return update_graph_scatter(df=filtered_df,column=column,per="MONTH")

#### Callback for distrito table
@app.callback(Output('table-mes-portal', 'data'),
	[Input('dropdown-portal-opciones-mes', 'value')])
def update_data_1(column):
    df_portal_mensual['Year'] = df_portal_mensual['Month'].apply(lambda x: x.split('-')[0])
    df_portal_mensual['Mes'] = df_portal_mensual['Month'].apply(lambda x: x.split('-')[1])
    filtered_df = pd.pivot_table(data=df_portal_mensual,values=column,index='Mes',columns='Year')
    filtered_df.columns = ['2018','2019']
    filtered_df = filtered_df.reset_index()
    filtered_df['Crecimiento'] = (filtered_df['2019']*100/filtered_df['2018'] - 100 ).round(2)
    filtered_df.fillna(0,inplace=True)
    filtered_df['Crecimiento'] = filtered_df['Crecimiento'].astype(str)+'%'
    filtered_df['Mes'] = filtered_df['Mes'].astype(int).map(string_months)
    filtered_df = filtered_df.to_dict("rows")
    return filtered_df

#### Update graph diaria Callback
@app.callback(
    Output('portal-dia', 'figure'),
    [Input('my-date-picker-single', 'date'),
     Input('dropdown-portal-opciones-dia', 'value')])
def update_graph_dia(date, column):
    date = pd.to_datetime(date)
    filtered_df = df_portal_diario[df_portal_diario.Date <= dt.strftime(date, "%Y-%m-%d")]
    filtered_df.sort_values(by='Date',ascending=False,inplace=True)
    filtered_df = filtered_df.iloc[0:60,:].reset_index(drop=True)
    filtered_df = filtered_df[['Date',column]]
    filtered_df = filtered_df.sort_values(by='Date').reset_index(drop=True)
    filtered_df['Date'] =  filtered_df['Date'].astype(str)
    trace = go.Scatter(
                x = filtered_df['Date'],
                y = filtered_df[column],

                name = column,
                mode = 'lines+markers+text',
                text = filtered_df[column],
                textposition='middle center',
                textfont=  dict(
                                 size=10,
                            ),
                marker = dict(
                                size = 3, color = colors[0],
                                line = dict(width = 1,)
                         )
            )
    layout = go.Layout(
            dict(
                title = "",
                legend_bgcolor = "rgb(255,255,255)",
                plot_bgcolor  = "rgb(255,255,255)",
                paper_bgcolor = "rgb(255,255,255)",
                #showlegend=True,
                margin=dict(t=50),

            )
    )
    data = [trace]
    return {
        "data": data,
        "layout": layout
    }
