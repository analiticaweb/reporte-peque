import dash_core_components as dcc
import dash_html_components as html
import dash_table
from components import Header, print_button
import datetime as dt
from datetime import datetime as dt
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objs as go

from components import temp_var

colors = ['#9079b7','#4179bd','#00a94f','#ffd200','#00a6cb','#0d5409','#d77233','#bdefdd','#efba7b']
############################ Start carga datos Claves ############################
# Ingreso de claves - Carga de datos
df_claves_cat = pd.read_csv("data/df_claves_cat.csv")

# Variables temporales
df_claves_cat = temp_var(df=df_claves_cat)

#Año y mes actual
df_max_date_claves = df_claves_cat[df_claves_cat["DATE"]==df_claves_cat["DATE"].max()].reset_index(drop=True)
df_max_date_claves = df_max_date_claves.loc[0,["DATE","YEAR","MONTH","DAY"]]
current_year_claves = df_max_date_claves['YEAR']
current_date_claves = df_max_date_claves['DATE']
day_of_month_claves = int(df_max_date_claves['DAY'])
initial_visible_month_claves = dt(current_year_claves,(current_date_claves - timedelta(days=day_of_month_claves) - timedelta(days=90)).month,1)
############################ End carga datos Claves ############################

############################ Start carga datos Redenciones ############################

#Por lugar de compra
df_red_lug = pd.read_csv('data/df_red_lug.csv')
# Variables temporales
df_red_lug = temp_var(df=df_red_lug)
#Año y mes actual
df_max_date_red = df_red_lug[df_red_lug["DATE"]==df_red_lug["DATE"].max()].reset_index(drop=True)
df_max_date_red = df_red_lug.loc[0,["DATE","YEAR","MONTH","DAY"]]
current_year_red = df_max_date_red['YEAR']
current_date_red = df_max_date_red['DATE']
day_of_month_red = int(df_max_date_red['DAY'])
initial_visible_month_red = dt(current_year_red,(current_date_red - timedelta(days=day_of_month_red) - timedelta(days=90)).month,1)

############################ End carga datos Redenciones ############################

############################ Start carga datos métricas del portal ############################

#Por lugar de compra
df_portal_diario = pd.read_csv('data/df_portal_diario.csv')
# Variables temporales
df_portal_diario['Date'] = pd.to_datetime(df_portal_diario['Date'])
df_portal_diario['MONTH'] = df_portal_diario['Date'].dt.month
df_portal_diario['YEAR'] = df_portal_diario['Date'].dt.year
df_portal_diario['DAY'] = df_portal_diario['Date'].dt.day
#Año y mes actual
df_max_date_portal = df_portal_diario[df_portal_diario["Date"]==df_portal_diario["Date"].max()].reset_index(drop=True)
df_max_date_portal = df_max_date_portal.loc[0,["Date","YEAR","MONTH","DAY"]]
current_year_portal = df_max_date_portal['YEAR']
current_date_portal = df_max_date_portal['Date']
day_of_month_portal = int(df_max_date_portal['DAY'])
initial_visible_month_portal = dt(current_year_portal,(current_date_portal - timedelta(days=day_of_month_portal) - timedelta(days=90)).month,1)

############################ End carga datos métricas del portal ###########################


############################ Start carga datos Registros ############################

#Por lugar de compra
df_registros = pd.read_csv('data/df_registros.csv')
# Variables temporales
df_registros["DATE"] = pd.to_datetime(df_registros["FECHA_INSCRIPCION"])
df_registros["MONTH"] = df_registros["DATE"].dt.month
df_registros["YEAR"] = df_registros["DATE"].dt.year
df_registros["DAY"] = df_registros["DATE"].dt.day

#Año y mes actual
df_max_date_registros = df_registros[df_registros["DATE"]==df_registros["DATE"].max()].reset_index(drop=True)
df_max_date_registros = df_max_date_registros.loc[0,["DATE","YEAR","MONTH","DAY"]]
current_year_registros = df_max_date_registros['YEAR']
current_date_registros = df_max_date_registros['DATE']
day_of_month_registros = int(df_max_date_registros['DAY'])
initial_visible_month_registros = dt(current_year_registros,(current_date_registros - timedelta(days=day_of_month_registros) - timedelta(days=90)).month,1)


string_months = {1:'Enero',2:'Febrero',3:'Marzo', 4:'Abril',5:'Mayo',6:'Junio', 7:'Julio',
                 8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre',}
df_activos_his = pd.read_csv('data/df_activos_his.csv',sep=';')
df_activos_his_ = df_activos_his.copy()
df_activos_his_['Mes'] = df_activos_his_['Mes'].map(string_months)

years = list(df_activos_his["Year"].sort_values(ascending=False).unique())
n = len(years)
data = []

for i in range(n):
    trace = go.Scatter(
            x = df_activos_his[df_activos_his["Year"]==years[i]]['Mes'].copy().map(string_months),
            y = df_activos_his[df_activos_his["Year"]==years[i]]['Activos'],

            name = str(years[i]),
            mode = 'lines+markers+text',
            text = df_activos_his[df_activos_his["Year"]==years[i]]['Activos'],
            #textposition='middle center',
            textfont=  dict(
                             size=10,
                        ),
            marker = dict(
                            size = 3, color = colors[i],
                            line = dict(width = 1,)
                     )
        )
    data.append(trace)

layout = go.Layout(
        dict(
            title = "",
            legend_bgcolor = "rgb(255,255,255)",
            plot_bgcolor  = "rgb(255,255,255)",
            paper_bgcolor = "rgb(255,255,255)",
            showlegend=True,
            margin=dict(t=50),

        )
)

############################ End carga datos Registros ############################


########################################################################
######################## START Layout Registros ########################
layout_Registros = html.Div(
                        [
                            #Page1

                            #Cabecera
                            html.Div(
                                [
                                    Header(),
                                    html.H3(
                                        ["Análitico de registros y activos"], className="subtitle"
                                    ),
                                    html.Div(
                                        [

                                            html.Div(
                                                [
                                                html.H4(
                                                    ["Seleccione el intervalo de tiempo"], className="subtitle padded"
                                                ),
                                                dcc.DatePickerRange(
                                                      id='my-date-picker-range-registros',
                                                      # with_portal=True,
                                                      min_date_allowed = df_registros['DATE'].min().to_pydatetime(),
                                                      max_date_allowed = df_registros['DATE'].max().to_pydatetime(),
                                                      initial_visible_month = initial_visible_month_registros,
                                                      start_date = pd.to_datetime('2018-01-01').to_pydatetime(),
                                                      end_date = df_registros['DATE'].max().to_pydatetime(),
                                                      number_of_months_shown = 4,
                                                ),
                                                html.Div(
                                                            id='output-container-date-picker-registros',
                                                            children="",
                                                            className='textBariol'
                                                )
                                                ], className='four columns'
                                            ),
                                            html.Div(
                                                [
                                                html.H4(
                                                    ["Seleccione la región"], className="subtitle padded"
                                                ),
                                                dcc.RadioItems(
                                                            id = 'items-options-distrito-registros',
                                                            options = [
                                                                {'label': 'Todas', 'value': 'TODOS'},
                                                                {'label': 'Personalizar', 'value': 'PERSONALIZAR'},
                                                            ],
                                                            value='TODOS',
                                                            labelStyle={'display': 'inline-block'},
                                                            className='textBariol'
                                                ),
                                                dcc.Dropdown(
                                                    id = 'dropdown-distritos-registros',
                                                    options=[
                                                        {'label': 'Cundi-Boyacá', 'value': 'CUNDI-BOY'},
                                                        {'label': 'Antioquia', 'value': 'ANTIOQUIA'},
                                                        {'label': 'Centro', 'value': 'CENTRO'},
                                                        {'label': 'Pacífico', 'value': 'PACIFICO'},
                                                        {'label': 'Atlantico', 'value': 'ATLANTICO'},
                                                        {'label': 'Santanderes', 'value': 'SANTANDERES'},
                                                        {'label': 'Eje Cafetero', 'value': 'EJE CAFETERO'},
                                                        {'label': 'Llanos', 'value': 'LLANOS'},
                                                        {'label': 'Otros', 'value': 'OTROS'},
                                                    ],
                                                    multi = True
                                                ),
                                                ], className="eight columns"
                                            ),
                                        ], className="row containerData"
                                    )

                                ]
                            ),
                            #SubPage
                            html.Div(
                                [
                                #Row1 Distribución en el tiempo
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                        [
                                                            html.H4(
                                                                ["Distribución a través del tiempo"], className="subtitle padded"
                                                            ),
                                                            dcc.RadioItems(
                                                                        id = 'items-options-total_registros_primer',
                                                                        options = [
                                                                            {'label': 'Registros Nuevos', 'value': 'REGISTROS'},
                                                                            {'label': 'Primer Contacto', 'value': 'PRIMER'},
                                                                            {'label': 'Total', 'value': 'TOT'},
                                                                        ],
                                                                        value='REGISTROS',
                                                                        labelStyle={'display': 'inline-block'}
                                                            ),

                                                        ],
                                                    ),
                                                html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                html.H5(
                                                                    ["Distribución por mes"], className="subtitle padded"
                                                                ),
                                                                dcc.Graph(id='registros-mes'),
                                                                ],
                                                            ),
                                                            html.Div(
                                                                [
                                                                html.H5(
                                                                    ["Distribución por día (último mes)"], className="subtitle padded"
                                                                ),
                                                                dcc.Graph(id='registros-dia'),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                            ], className="eight columns"
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                    html.H4(
                                                        ["Total Acumulado"], className="subtitle padded"
                                                    ),
                                                    dash_table.DataTable(
                                                          id='total-table-registros',
                                                          columns=[
                                                                    {'name': 'Indicador', 'id': 'Indicador'},
                                                                    {'name': 'Total', 'id': 'Total'},
                                                                  ],
                                                          editable=True,
                                                          # sorting=True,
                                                          # sorting_type="multi",
                                                          style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                          style_table={
                                                                            'maxHeight': '200px',
                                                                            'overflowY': 'scroll'
                                                                        },
                                                    ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                    html.H4(
                                                        ["Acumulados por mes"], className="subtitle padded"
                                                    ),
                                                    dash_table.DataTable(
                                                          id='mes-table-registros',
                                                          columns=[
                                                                    {"name": "Año", "id": "Año"},
                                                                    {"name": "Mes", "id": "Mes"},
                                                                    {"name": "Registros", "id": "Registros Nuevos"},
                                                                    {"name": "Primer Contacto", "id": "Primer Contacto"},
                                                                    {"name": "Total", "id": "Total"},
                                                                  ],
                                                          editable=True,
                                                          # sorting=True,
                                                          # sorting_type="multi",
                                                          style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                          style_table={
                                                                            'maxHeight': '440px',
                                                                            'overflowY': 'scroll',
                                                                        },
                                                    ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                    html.H4(
                                                        ["Acumulados por día (último mes)"], className="subtitle padded"
                                                    ),
                                                    dash_table.DataTable(
                                                          id='dia-table-registros',
                                                          columns=[
                                                                    {"name": "Año", "id": "Año"},
                                                                    {"name": "Dia", "id": "Dia"},
                                                                    {"name": "Registros Nuevos", "id": "REGISTROS"},
                                                                    {"name": "Primer Contacto", "id": "PRIMER"},
                                                                    {"name": "Total", "id": "TOT"},
                                                                  ],
                                                          editable=True,
                                                          # sorting=True,
                                                          # sorting_type="multi",
                                                          style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                          style_table={
                                                                            'maxHeight': '380px',
                                                                            'overflowY': 'scroll',
                                                                        },
                                                    ),
                                                    ]
                                                ),
                                            ], className="four columns"
                                        ),
                                    ], className="row containerData"
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Inscritos por Distrito"], className="subtitle padded"
                                                        ),
                                                        dcc.Graph('registros-distritos')
                                                    ],className='eight columns'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Inscritos por Ciudad"], className="subtitle padded"
                                                        ),
                                                        dash_table.DataTable(
                                                              id='ciudad-table-registros',
                                                              columns=[
                                                                        {"name": "Distrito", "id": "DISTRITO"},
                                                                        {"name": "Ciudad", "id": "CIUDAD"},
                                                                        {"name": "Registros Nuevos", "id": "VISITORID"},
                                                                        {"name": "% Total Registros", "id": "% Total Registros"},
                                                                      ],
                                                              editable=True,
                                                              # sorting=True,
                                                              # sorting_type="multi",
                                                              style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                              style_table={
                                                                                'maxHeight': '380px',
                                                                                'overflowY': 'scroll',
                                                                            },
                                                        ),
                                                    ],className='four columns'
                                                ),
                                            ],className='Row'
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Etapa de los inscritos"], className="subtitle padded"
                                                        ),
                                                        dcc.Graph('registros-edad')
                                                    ],className='six columns'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Medio de inscripción"], className="subtitle padded"
                                                        ),
                                                        dcc.Graph('registros-medio')
                                                    ],className='six columns'
                                                ),
                                            ],className='Row'
                                        )
                                    ], className="row containerData"
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [   html.H4(
                                                    ["Activos"], className="subtitle padded"
                                                ),
                                                dash_table.DataTable(
                                                      id='table-total-activos',
                                                      columns=[
                                                                {"name": "Segmento", "id": "Segmento"},
                                                                {"name": "Número de Usuarios", "id": "Número de Usuarios"}
                                                              ],
                                                      editable=True,
                                                      # sorting=True,
                                                      # sorting_type="multi",
                                                      style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                      style_table={
                                                                        'maxHeight': '380px',
                                                                        'overflowY': 'scroll',

                                                                    },
                                                ),
                                            ],className='row'
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Activos por Etapa"], className="subtitle padded"
                                                        ),
                                                        dcc.Graph('activos-etapa')
                                                    ],
                                                ),
                                            ],className='Row'
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Activos por Distrito"], className="subtitle padded"
                                                        ),
                                                        dcc.Graph('activos-distrito')
                                                    ],className='six columns'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Activos por Ciudad"], className="subtitle padded"
                                                        ),
                                                        dash_table.DataTable(
                                                              id='ciudad-table-activos',
                                                              columns=[
                                                                        {"name": "Distrito", "id": "DISTRITO"},
                                                                        {"name": "Ciudad", "id": "CIUDAD"},
                                                                        {"name": "Activos", "id": "VISITORID"},
                                                                        {"name": "% Total Activos", "id": "% Total Activos"},
                                                                      ],
                                                              editable=True,
                                                              # sorting=True,
                                                              # sorting_type="multi",
                                                              style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                              style_table={
                                                                                'maxHeight': '380px',
                                                                                'overflowY': 'scroll',

                                                                            },
                                                        ),
                                                    ],className='six columns'
                                                ),
                                            ],className='Row'
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Activos por mes y año (tendencia)"], className="subtitle padded"
                                                        ),
                                                        dcc.Graph(id='activos-mes-year-graph',
                                                            figure = {"data": data,"layout": layout},
                                                        )
                                                    ],className='eight columns'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Activos por mes y año"], className="subtitle padded"
                                                        ),
                                                        dash_table.DataTable(
                                                              id='activos-mes-year',
                                                              columns=[
                                                                        {"name": "Año", "id": "Year"},
                                                                        {"name": "Mes", "id": "Mes"},
                                                                        {"name": "Activos", "id": "Activos"},
                                                                      ],
                                                              editable=True,
                                                              # sorting=True,
                                                              # sorting_type="multi",
                                                              style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                              style_table={
                                                                                'maxHeight': '390px',
                                                                                'overflowY': 'scroll',
                                                                            },
                                                            data = df_activos_his_.to_dict("rows"),

                                                        ),
                                                    ],className='four columns'
                                                ),
                                            ],className='Row'
                                        ),
                                    ], className="row containerData"
                                )
                                ],className="sub_page"
                            ),
                        ],className="page"

                    )
######################## END Layout REGISTROS ########################
######################################################################

#####################################################################
######################## START Layout CLAVES ########################
layout_Claves = html.Div(
                    [
                        #Page2

                        #Cabecera
                        html.Div(
                            [
                                Header(),
                                html.H3(
                                    ["Análitico de ingreso del claves"], className="subtitle"
                                ),
                                html.Div(
                                    [

                                        html.Div(
                                            [
                                            html.H4(
                                                ["Seleccione el intervalo de tiempo"], className="subtitle padded"
                                            ),
                                            dcc.DatePickerRange(
                                                  id='my-date-picker-range-claves',
                                                  # with_portal=True,
                                                  min_date_allowed = df_claves_cat['DATE'].min().to_pydatetime(),
                                                  max_date_allowed = df_claves_cat['DATE'].max().to_pydatetime(),
                                                  initial_visible_month = initial_visible_month_claves,
                                                  start_date = pd.to_datetime('2018-01-01').to_pydatetime(),
                                                  end_date = df_claves_cat['DATE'].max().to_pydatetime(),
                                                  number_of_months_shown = 4,
                                            ),
                                            html.Div(
                                                        id='output-container-date-picker-claves',
                                                        children="",
                                                        className='textBariolñ'
                                            )
                                            ], className='four columns'
                                        ),
                                        html.Div(
                                            [
                                            html.H4(
                                                ["Seleccione la región"], className="subtitle padded"
                                            ),
                                            dcc.RadioItems(
                                                        id = 'items-options-distrito-claves',
                                                        options = [
                                                            {'label': 'Todas', 'value': 'TODOS'},
                                                            {'label': 'Personalizar', 'value': 'PERSONALIZAR'},
                                                        ],
                                                        value='TODOS',
                                                        labelStyle={'display': 'inline-block'},
                                                        className='textBariol'
                                            ),
                                            dcc.Dropdown(
                                                id = 'dropdown-distritos-claves',
                                                options=[
                                                    {'label': 'Cundi-Boyacá', 'value': 'CUNDI-BOY'},
                                                    {'label': 'Antioquia', 'value': 'ANTIOQUIA'},
                                                    {'label': 'Centro', 'value': 'CENTRO'},
                                                    {'label': 'Pacífico', 'value': 'PACIFICO'},
                                                    {'label': 'Atlantico', 'value': 'ATLANTICO'},
                                                    {'label': 'Santanderes', 'value': 'SANTANDERES'},
                                                    {'label': 'Eje Cafetero', 'value': 'EJE CAFETERO'},
                                                    {'label': 'Llanos', 'value': 'LLANOS'},
                                                    {'label': 'Otros', 'value': 'OTROS'},
                                                ],
                                                multi = True
                                            ),
                                            ], className="eight columns"
                                        ),
                                    ], className="row containerData"
                                )

                            ]
                        ),
                        #SubPage
                        html.Div(
                            [
                            #Row1 Distribución en el tiempo
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                    [
                                                        html.H4(
                                                            ["Distribución a través del tiempo"], className="subtitle padded"
                                                        ),
                                                        dcc.RadioItems(
                                                                    id = 'items-options-clav_pun',
                                                                    options = [
                                                                        {'label': 'Claves Ingresadas', 'value': 'CLAVES'},
                                                                        {'label': 'Puntos Acumulados', 'value': 'PUNTOS'},
                                                                    ],
                                                                    value='CLAVES',
                                                                    labelStyle={'display': 'inline-block'}
                                                        ),

                                                    ],
                                                ),
                                            html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                            html.H5(
                                                                ["Distribución por mes"], className="subtitle padded"
                                                            ),
                                                            dcc.Graph(id='claves-mes'),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            [
                                                            html.H5(
                                                                ["Distribución por día (último mes)"], className="subtitle padded"
                                                            ),
                                                            dcc.Graph(id='claves-dia'),
                                                            ]
                                                        )
                                                    ]
                                                ),
                                        ], className="eight columns"
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                html.H4(
                                                    ["Total Acumulado"], className="subtitle padded"
                                                ),
                                                dash_table.DataTable(
                                                      id='total-table-claves',
                                                      columns=[
                                                                {"name": "Indicador", "id": "Indicador"},
                                                                {"name": "Total", "id": "Total"},
                                                              ],
                                                      editable=True,
                                                      # sorting=True,
                                                      # sorting_type="multi",
                                                      style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                      style_table={
                                                                        'maxHeight': '200px',
                                                                        'overflowY': 'scroll',
                                                                    },
                                                ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                html.H4(
                                                    ["Acumulados por mes"], className="subtitle padded"
                                                ),
                                                dash_table.DataTable(
                                                      id='mes-table-claves',
                                                      columns=[
                                                                {"name": "Año", "id": "Año"},
                                                                {"name": "Mes", "id": "Mes"},
                                                                {"name": "Claves", "id": "Claves"},
                                                                {"name": "Puntos", "id": "Puntos"}
                                                              ],
                                                      editable=True,
                                                      # sorting=True,
                                                      # sorting_type="multi",
                                                      style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                      style_table={
                                                                        'maxHeight': '440px',
                                                                        'overflowY': 'scroll',
                                                                    },
                                                ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                html.H4(
                                                    ["Acumulados por día (último mes)"], className="subtitle padded"
                                                ),
                                                dash_table.DataTable(
                                                      id='dia-table-claves',
                                                      columns=[
                                                                {"name": "Año", "id": "Año"},
                                                                {"name": "Día", "id": "Día"},
                                                                {"name": "Claves", "id": "Claves"},
                                                                {"name": "Puntos", "id": "Puntos"}
                                                              ],
                                                      editable=True,
                                                      # sorting=True,
                                                      # sorting_type="multi",
                                                      style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                      style_table={
                                                                        'maxHeight': '380px',
                                                                        'overflowY': 'scroll',
                                                                    },
                                                ),
                                                ]
                                            ),
                                        ], className="four columns"
                                    ),
                                ], className="row containerData"
                            ),
                            #Row2 Distribución distritos y por tipo de producto
                            html.Div(
                                [
                                    html.Div(
                                    [
                                        html.Div(
                                            [
                                            html.H4(
                                                ["Distribución por distrito"], className="subtitle padded"
                                            ),
                                            dcc.RadioItems(
                                                        id = 'items-options-clav_pun-distrito',
                                                        options = [
                                                            {'label': 'Claves Ingresadas', 'value': 'CLAVES'},
                                                            {'label': 'Puntos Acumulados', 'value': 'PUNTOS'},
                                                        ],
                                                        value='CLAVES',
                                                        labelStyle={'display': 'inline-block'}
                                            ),
                                            dcc.Graph(id="claves-distrito"),
                                            html.H4(
                                                    ["Acumulados por ciudad"], className="subtitle padded"
                                            ),
                                            dash_table.DataTable(
                                                      id='distrito-table-claves',
                                                      columns=[
                                                                {"name": "Distrito", "id": "DISTRITO"},
                                                                {"name": "Ciudad", "id": "CIUDAD"},
                                                                {"name": "Claves", "id": "CLAVES"},
                                                                {"name": "% Total Claves", "id": "% Total Claves"},
                                                                {"name": "Puntos", "id": "PUNTOS"},
                                                                {"name": "% Total Puntos", "id": "% Total Puntos"},
                                                              ],
                                                      editable=True,
                                                      # sorting=True,
                                                      # sorting_type="multi",
                                                      style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                      style_table={
                                                                        'maxHeight': '450px',
                                                                        'overflowY': 'scroll',
                                                                    },
                                            ),
                                            ],className="six columns"
                                        ),
                                        html.Div(
                                            [
                                            html.H4(
                                                ["Distribución por categoría del producto"], className="subtitle padded"
                                            ),
                                            dcc.RadioItems(
                                                        id = 'items-options-clav_pun-TipoPro',
                                                        options = [
                                                            {'label': 'Claves Ingresadas', 'value': 'CLAVES'},
                                                            {'label': 'Puntos Acumulados', 'value': 'PUNTOS'},
                                                        ],
                                                        value='CLAVES',
                                                        labelStyle={'display': 'inline-block'}
                                            ),
                                            html.H5(
                                                ["Distribución total"], className="subtitle padded"
                                            ),
                                            dcc.Graph(id="claves-tipo-total"),
                                            html.H5(
                                                ["Distribución diária (último mes)"], className="subtitle padded"
                                            ),
                                            dcc.Graph(id="claves-tipo-dia"),
                                            ],className="six columns"
                                        ),
                                    ], className="row"
                                    ),
                                    html.Div(
                                        [
                                            html.H4(
                                                    ["Distribución por categorias, segmentos y subsegmentos"], className="subtitle padded"
                                            ),
                                            dash_table.DataTable(
                                                      id='cat_seg_subseg-table-claves',
                                                      columns=[
                                                                {"name": "Categorias", "id": "Clasificacion"},
                                                                {"name": "Segmento", "id": "SEGMENTO"},
                                                                {"name": "Subsegmento", "id": "SUBSEGMENTO"},
                                                                {"name": "Claves", "id": "CLAVES"},
                                                                {"name": "% Total Claves", "id": "% Total Claves"},
                                                                {"name": "Puntos", "id": "PUNTOS"},
                                                                {"name": "% Total Puntos", "id": "% Total Puntos"},
                                                              ],
                                                      editable=True,
                                                      # sorting=True,
                                                      # sorting_type="multi",
                                                      style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                      style_table={
                                                                        'maxHeight': '350px',
                                                                        'overflowY': 'scroll',
                                                                        'border': 'thin lightgrey solid'
                                                                    },
                                            ),
                                        ], className="row"
                                    ),
                                    html.Div(
                                        [
                                            html.H4(
                                                    ["Distribución por medio"], className="subtitle padded"
                                            ),
                                            dcc.RadioItems(
                                                        id = 'items-options-clav_pun-medio',
                                                        options = [
                                                            {'label': 'Claves Ingresadas', 'value': 'CLAVES'},
                                                            {'label': 'Puntos Acumulados', 'value': 'PUNTOS'},
                                                        ],
                                                        value='CLAVES',
                                                        labelStyle={'display': 'inline-block'}
                                            ),
                                            dcc.Graph(id="claves-medio"),
                                        ], className="row"
                                    )
                                ], className="row containerData"
                            ),
                            ],className="sub_page"
                        ),
                    ],className="page"
                )
######################## END Layout CLAVES ########################
###################################################################

##########################################################################
######################## START Layout REDENCIONES ########################
layout_Redenciones = html.Div(
                        [
                            #Page3

                            #Cabecera
                            html.Div(
                                [
                                    Header(),
                                    html.H3(
                                        ["Análitico de las redenciones"], className="subtitle"
                                    ),
                                    html.Div(
                                        [

                                            html.Div(
                                                [
                                                html.H4(
                                                    ["Seleccione el intervalo de tiempo"], className="subtitle padded"
                                                ),
                                                dcc.DatePickerRange(
                                                      id='my-date-picker-range-redenciones',
                                                      # with_portal=True,
                                                      min_date_allowed = df_red_lug['DATE'].min().to_pydatetime(),
                                                      max_date_allowed = df_red_lug['DATE'].max().to_pydatetime(),
                                                      initial_visible_month = initial_visible_month_red,
                                                      start_date = pd.to_datetime('2018-01-01').to_pydatetime(),
                                                      end_date = df_red_lug['DATE'].max().to_pydatetime(),
                                                      number_of_months_shown = 4,
                                                ),
                                                html.Div(
                                                            id='output-container-date-picker-redenciones',
                                                            children="",
                                                            className='textBariol'
                                                )
                                                ], className='four columns'
                                            ),
                                            html.Div(
                                                [
                                                html.H4(
                                                    ["Seleccione la región"], className="subtitle padded"
                                                ),
                                                dcc.RadioItems(
                                                            id = 'items-options-distrito-redenciones',
                                                            options = [
                                                                {'label': 'Todas', 'value': 'TODOS'},
                                                                {'label': 'Personalizar', 'value': 'PERSONALIZAR'},
                                                            ],
                                                            value='TODOS',
                                                            labelStyle={'display': 'inline-block'},
                                                            className='textBariol'
                                                ),
                                                dcc.Dropdown(
                                                    id = 'dropdown-distritos-redenciones',
                                                    options=[
                                                        {'label': 'Cundi-Boyacá', 'value': 'CUNDI-BOY'},
                                                        {'label': 'Antioquia', 'value': 'ANTIOQUIA'},
                                                        {'label': 'Centro', 'value': 'CENTRO'},
                                                        {'label': 'Pacífico', 'value': 'PACIFICO'},
                                                        {'label': 'Atlantico', 'value': 'ATLANTICO'},
                                                        {'label': 'Santanderes', 'value': 'SANTANDERES'},
                                                        {'label': 'Eje Cafetero', 'value': 'EJE CAFETERO'},
                                                        {'label': 'Llanos', 'value': 'LLANOS'},
                                                        {'label': 'Otros', 'value': 'OTROS'},
                                                    ],
                                                    multi = True
                                                ),
                                                ], className="eight columns"
                                            ),
                                        ], className="row containerData"
                                    )

                                ]
                            ),
                            #Subpage
                            html.Div(
                                [
                                #Row1 Transaccional
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                        [
                                                            html.H4(
                                                                ["Distribución a través del tiempo"], className="subtitle padded"
                                                            ),
                                                            dcc.RadioItems(
                                                                        id = 'items-options-red_puntos',
                                                                        options = [
                                                                            {'label': 'Número de Redenciones', 'value': 'RED'},
                                                                            {'label': 'Puntos Redimidos', 'value': 'PUNTOS'},
                                                                        ],
                                                                        value='RED',
                                                                        labelStyle={'display': 'inline-block'}
                                                            ),

                                                            dcc.RadioItems(
                                                                        id = 'items-options-redt_redf_redv',
                                                                        options = [
                                                                            {'label': 'Totales', 'value': 'RED_TOT'},
                                                                            {'label': 'Físicas', 'value': 'RED_FIS'},
                                                                            {'label': 'Virtuales', 'value': 'RED_VIR'},
                                                                            {'label': 'Regalos', 'value': 'RED_REG'},
                                                                        ],
                                                                        value='RED_TOT',
                                                                        labelStyle={'display': 'inline-block'}
                                                            ),

                                                        ],
                                                    ),
                                                html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                html.H5(
                                                                    ["Distribución por mes"], className="subtitle padded"
                                                                ),
                                                                dcc.Graph(id='redenciones-mes'),
                                                                ],
                                                            ),
                                                            html.Div(
                                                                [
                                                                html.H5(
                                                                    ["Distribución por día (último mes)"], className="subtitle padded"
                                                                ),
                                                                dcc.Graph(id='redenciones-dia'),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                            ], className="eight columns"
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                    html.Div(
                                                            [
                                                                html.H4(
                                                                    ["Tablas Indicadores"], className="subtitle padded"
                                                                ),

                                                                dcc.RadioItems(
                                                                            id = 'items-options-redt_redf_redv-tabla',
                                                                            options = [
                                                                                {'label': 'Totales', 'value': 'TOT'},
                                                                                {'label': 'Físicas', 'value': 'FIS'},
                                                                                {'label': 'Virtuales', 'value': 'VIR'},
                                                                                {'label': 'Regalos', 'value': 'REG'},
                                                                            ],
                                                                            value='TOT',
                                                                            labelStyle={'display': 'inline-block'}
                                                                ),

                                                            ],
                                                    ),
                                                    html.H5(
                                                        ["Total Acumulado"], className="subtitle padded"
                                                    ),
                                                    dash_table.DataTable(
                                                          id='total-table-redenciones',
                                                          columns=[
                                                                    {"name": "Indicador", "id": "Indicador"},
                                                                    {"name": "Total", "id": "Total"},
                                                                  ],
                                                          editable=True,
                                                          # sorting=True,
                                                          # sorting_type="multi",
                                                          style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                          style_table={
                                                                            'maxHeight': '200px',
                                                                            'overflowY': 'scroll',
                                                                        },
                                                    ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                    html.H5(
                                                        ["Acumulados por mes"], className="subtitle padded"
                                                    ),
                                                    dash_table.DataTable(
                                                          id='mes-table-redenciones',
                                                          columns=[
                                                                    {"name": "Año", "id": "Año"},
                                                                    {"name": "Mes", "id": "Mes"},
                                                                    {"name": "Redenciones", "id": "Redenciones"},
                                                                    {"name": "Puntos", "id": "Puntos"}
                                                                  ],
                                                          editable=True,
                                                          # sorting=True,
                                                          # sorting_type="multi",
                                                          style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                          style_table={
                                                                            'maxHeight': '440px',
                                                                            'overflowY': 'scroll',
                                                                        },
                                                    ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                    html.H5(
                                                        ["Acumulados por día (último mes)"], className="subtitle padded"
                                                    ),
                                                    dash_table.DataTable(
                                                          id='dia-table-redenciones',
                                                          columns=[
                                                                    {"name": "Año", "id": "Año"},
                                                                    {"name": "Día", "id": "Día"},
                                                                    {"name": "Redenciones", "id": "Redenciones"},
                                                                    {"name": "Puntos", "id": "Puntos"}
                                                                  ],
                                                          editable=True,
                                                          # sorting=True,
                                                          # sorting_type="multi",
                                                          style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                          style_table={
                                                                            'maxHeight': '380px',
                                                                            'overflowY': 'scroll',
                                                                        },
                                                    ),
                                                    ]
                                                ),
                                            ], className="four columns"
                                        ),
                                    ], className="row containerData"
                                ),
                                #Row2 Distribución por distritos y por tipo de producto
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            ["Distribución por distrito"], className="subtitle padded"
                                                        ),
                                                        dcc.RadioItems(
                                                                    id = 'items-options-red_puntos-dist',
                                                                    options = [
                                                                        {'label': 'Número de Redenciones', 'value': 'RED'},
                                                                        {'label': 'Puntos Redimidos', 'value': 'PUNTOS'},
                                                                    ],
                                                                    value='RED',
                                                                    labelStyle={'display': 'inline-block'}
                                                        ),

                                                        dcc.RadioItems(
                                                                    id = 'items-options-redt_redf_redv-dist',
                                                                    options = [
                                                                        {'label': 'Totales', 'value': 'RED_TOT'},
                                                                        {'label': 'Físicas', 'value': 'RED_FIS'},
                                                                        {'label': 'Virtuales', 'value': 'RED_VIR'},
                                                                        {'label': 'Regalos', 'value': 'RED_REG'},
                                                                    ],
                                                                    value='RED_TOT',
                                                                    labelStyle={'display': 'inline-block'}
                                                        ),
                                                        dcc.Graph(id="redenciones-distrito"),
                                                    ],className='six columns'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                                ["Distribución por ciudad"], className="subtitle padded"
                                                        ),
                                                        dcc.RadioItems(
                                                                    id = 'items-options-redt_redf_redv-tabla-dist',
                                                                    options = [
                                                                        {'label': 'Totales', 'value': 'TOT'},
                                                                        {'label': 'Físicas', 'value': 'FIS'},
                                                                        {'label': 'Virtuales', 'value': 'VIR'},
                                                                        {'label': 'Regalos', 'value': 'REG'},
                                                                    ],
                                                                    value='TOT',
                                                                    labelStyle={'display': 'inline-block'}
                                                        ),
                                                        dash_table.DataTable(
                                                                  id='distrito-table-redenciones',
                                                                  columns=[
                                                                            {"name": "Distrito", "id": "DISTRITO"},
                                                                            {"name": "Ciudad", "id": "CIUDAD"},
                                                                            {"name": "Redenciones", "id": "RED"},
                                                                            {"name": "% Total Redenciones", "id": "% Total Redenciones"},
                                                                            {"name": "Puntos", "id": "PUNTOS"},
                                                                            {"name": "% Total Puntos", "id": "% Total Puntos"},
                                                                          ],
                                                                  editable=True,
                                                                  # sorting=True,
                                                                  # sorting_type="multi",
                                                                  style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                                  style_table={
                                                                                    'maxHeight': '450px',
                                                                                    'overflowY': 'scroll',
                                                                                },
                                                        ),
                                                    ],className='six columns'
                                                ),
                                            ],className="row"
                                        ),
                                        html.Div(
                                            [
                                                html.H4(
                                                        ["Distribución por punto de redención"], className="subtitle padded"
                                                ),
                                                dcc.RadioItems(
                                                            id = 'items-options-redt_redf_redv-tabla-punto_red',
                                                            options = [
                                                                {'label': 'Físicas', 'value': 'FIS'},
                                                            ],
                                                            value='FIS',
                                                            labelStyle={'display': 'inline-block'}
                                                ),
                                                dash_table.DataTable(
                                                          id='punto_red-table-redenciones',
                                                          columns=[
                                                                    #{"name": "Distrito", "id": "DISTRITO"},
                                                                    {"name": "Punto de redención", "id": "LUGAR_COMPRA"},
                                                                    {"name": "Redenciones", "id": "RED"},
                                                                    {"name": "% Total Redenciones", "id": "% Total Redenciones"},
                                                                    {"name": "Puntos", "id": "PUNTOS"},
                                                                    {"name": "% Total Puntos", "id": "% Total Puntos"},
                                                                  ],
                                                          editable=True,
                                                          # sorting=True,
                                                          # sorting_type="multi",
                                                          style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                          style_table={
                                                                            'maxHeight': '450px',
                                                                            'overflowY': 'scroll',
                                                                        },
                                                ),
                                            ],className="row"
                                        )

                                    ], className="row containerData"
                                )
                                ],className="sub_page"
                            ),

                        ],    className="page"
                    )
######################## END Layout Redenciones ########################

######################## START Layout Trafico ########################
layout_Trafico = html.Div(
                    [
                        #Cabecera
                        html.Div(
                            [
                                Header(),
                                html.H3(
                                    ["Análitico de las métricas del portal"], className="subtitle"
                                ),
                            ],
                        ),
                        #Análisis T
                        html.Div(
                            [
                                html.H4("Descripción de las métricas incluidas en el reporte", className="subtitle padded"),
                                html.Div(
                                        [   html.Li(
                                            [
                                                html.Span("Usuarios:", className="bold"),
                                                html.Span(' número de usuarios que ingresan al portal.')
                                            ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span("Sesiones:", className="bold"),
                                                    html.Span(''' número de visitas de los usarios al portal de Pequeñín. Por ejemplo,
                                                                  un usario que entra tres veces al día al portal genera 3 sesiones,
                                                                  pero si estas 3 visitas son realizadas dentro de un intervalo de media
                                                                  hora  el usuario solo genera una sesión''')
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span("Páginas vistas:", className="bold"),
                                                    html.Span(' número de páginas vistas por los usuarios en las sesiones')
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span("Promedio de permamanecia:", className="bold"),
                                                    html.Span(''' suma de los tiempos de permanencia de todos los usarios dividio
                                                                  el número total de usarios, medido en minutos''')
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span("Tasa de rebote proemdio:", className="bold"),
                                                    html.Span(''' es la división entre el número de usarios que no gneraron ninguna interacción
                                                                  en el portal y el número de usarios total''')
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span("Nuevos usarios:", className="bold"),
                                                    html.Span(''' número de usarios que ingresan al portal por primera vez,
                                                                  y usarios que habían entrado previamente pero que borraron su registro de cookies de navegación''')
                                                ], className=''
                                            ),
                                            html.Li(
                                                [
                                                    html.Span("Usarios recurrentes:", className="bold"),
                                                    html.Span(''' número de usarios que han generado más de una sesión en el portal''')
                                                ]
                                            ),
                                        ],style = {"fontFamily": "Bariol"},
                                    ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H4(
                                                    ["Distribución por mes y año"], className="subtitle padded"
                                                ),
                                                dcc.Dropdown(
                                                    id = 'dropdown-portal-opciones-mes',
                                                    options=[
                                                                {'label': 'Sesiones', 'value': 'Sessions'},
                                                                {'label': 'Usuarios', 'value': 'Users'},
                                                                {'label': 'Páginas vistas', 'value': 'Pageviews'},
                                                                {'label': 'Promedio de permamanecia', 'value': 'Avg. session length (min)'},
                                                                {'label': 'Tasa de rebote promedio', 'value': 'Bounce rate'},
                                                                {'label': 'Nuevos usuarios', 'value': 'New users'},
                                                                {'label': 'Usuarios recurrentes', 'value': 'Usuarios recurrentes'},
                                                            ],
                                                    multi = False,
                                                    value = 'Sessions',
                                                ),
                                                 html.H5(
                                                     ["Tendencia mensual"], className="subtitle padded"
                                                 ),
                                                 dcc.Graph('portal-mes')
                                            ],className='row'
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    ["Crecimiento"], className="subtitle padded"
                                                ),
                                                dash_table.DataTable(
                                                      id='table-mes-portal',
                                                      columns=[
                                                                {"name": "Mes", "id": "Mes"},
                                                                {"name": "2018", "id": "2018"},
                                                                {"name": "2019", "id": "2019"},
                                                                {"name": "Crecimiento", "id": "Crecimiento"},
                                                              ],
                                                      editable=True,
                                                      # sorting=True,
                                                      # sorting_type="multi",
                                                      style_cell = {"fontFamily": "Bariol", 'textAlign': 'left'},
                                                      style_table={
                                                                        'maxHeight': '400px',
                                                                        'overflowY': 'scroll',
                                                                    },
                                                ),
                                            ],className='row'
                                        ),
                                    ],className='row'
                                ),
                                html.Div(
                                    [
                                        html.H4(
                                            ["Distribución por día"], className="subtitle padded"
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                                children="Seleccione una fecha. Se tendrán en cuenta 60 días atras de la fecha escogida",
                                                                className='textBariol'
                                                        ),
                                                        dcc.DatePickerSingle(
                                                              id='my-date-picker-single',
                                                              # with_portal=True,
                                                              min_date_allowed = df_portal_diario['Date'].min().to_pydatetime(),
                                                              max_date_allowed = df_portal_diario['Date'].max().to_pydatetime(),
                                                              initial_visible_month = initial_visible_month_portal,
                                                              date = df_portal_diario['Date'].max().to_pydatetime(),
                                                              number_of_months_shown = 1,
                                                        ),
                                                    ], className="six columns"
                                                ),
                                                html.Div(
                                                    [
                                                        html.Div(
                                                                    children="Seleccione una métrica",
                                                                    className='textBariol'
                                                        ),
                                                        dcc.Dropdown(
                                                            id = 'dropdown-portal-opciones-dia',
                                                            options=[
                                                                        {'label': 'Sesiones', 'value': 'Sessions'},
                                                                        {'label': 'Usuarios', 'value': 'Users'},
                                                                        {'label': 'Páginas vistas', 'value': 'Pageviews'},
                                                                        {'label': 'Promedio de permamanecia', 'value': 'Avg. session length (min)'},
                                                                        {'label': 'Tasa de rebote promedio', 'value': 'Bounce rate'},
                                                                        {'label': 'Nuevos usuarios', 'value': 'New users'},
                                                                        {'label': 'Usuarios recurrentes', 'value': 'Usuarios recurrentes'},
                                                                    ],
                                                            multi = False,
                                                            value = 'Sessions',
                                                        ),
                                                    ], className="six columns"
                                                ),
                                            ],className='row'
                                        ),
                                        html.Br(),
                                        dcc.Graph('portal-dia')
                                    ],className='row'
                                ),
                            ],className="row containerData"
                        ),
                    ],className="page"
                )

######################## END Layout Trafico ########################
