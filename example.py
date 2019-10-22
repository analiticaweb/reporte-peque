#######
# Here we'll use the mpg.csv dataset to demonstrate
# how multiple inputs can affect the same graph.
######
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime as dt
from datetime import date, timedelta
import plotly.graph_objs as go
import dash_table


app = dash.Dash()

pd.options.mode.chained_assignment = None

# Read in Travel Report Data
# Ingreso de claves - Carga de datos
string_months = {1:'Enero',2:'Febrero',3:'Marzo', 4:'Abril',5:'Mayo',6:'Junio', 7:'Julio',
                 8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre',}
cat_direc = {'PA?ALES':'Pañales','PA?ITOS':'Pañitos','CREMITAS':'Cremitas','OTROS':'Otros','CUPONES':'Cupones'}

colors = ['rgba(83, 196, 213, 1)','rgba(250, 231, 20, 1)','rgba(59, 28, 84, 1)','rgba(104, 50, 149, 1)',
          'rgba(165, 113, 208, 1)','rgba(212, 143, 230, 1)']
df_claves_cat = pd.read_csv("data/df_claves_cat.csv")
df_claves_cat["DATE"] = pd.to_datetime(df_claves_cat["FECHA"])
df_claves_cat["YEAR"] =  df_claves_cat["DATE"].dt.year
df_claves_cat["MONTH"] =  df_claves_cat["DATE"].dt.month
df_claves_cat["DAY"] = df_claves_cat["DATE"].dt.day

app.layout = html.Div([

        html.Div([
                dcc.DatePickerRange(
                      id='my-date-picker-range-claves',
                      # with_portal=True,
                      min_date_allowed=df_claves_cat['DATE'].min().to_pydatetime(),
                      max_date_allowed=df_claves_cat['DATE'].max().to_pydatetime(),
                      initial_visible_month=dt(df_claves_cat['YEAR'].max(),df_claves_cat['DATE'].max().to_pydatetime().month, 1),
                      start_date = dt(2018, 1, 1),
                      end_date = df_claves_cat['DATE'].max().to_pydatetime(),
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
                html.Div(
                    [
                    html.H6(
                        ["Seleccione la región"], className="subtitle padded"
                    ),
                    dcc.RadioItems(
                                id = 'items-options-distrito',
                                options = [
                                    {'label': 'Todas', 'value': 'TODOS'},
                                    {'label': 'Personalizar', 'value': 'PERSONALIZAR'},
                                ],
                                value='TODOS',
                                labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Dropdown(
                        id = 'dropdown-distritos',
                        options=[
                            {'label': 'Cundimarca', 'value': 'CUNDINAMARCA'},
                            {'label': 'Antioquia', 'value': 'ANTIOQUIA'},
                            {'label': 'Región Andina', 'value': 'REGION ANDINA'},
                            {'label': 'Región del Pacífico', 'value': 'REGION ORINOQUIA'},
                            {'label': 'Región Caribe', 'value': 'REGION CARIBE'},
                            {'label': 'Región Amazónica', 'value': 'REGION AMAZONICA'},
                            {'label': 'Región Atlantica', 'value': 'ATLANTICO'},
                            {'label': 'Otros', 'value': 'OTROS'},
                        ],
                        multi = 'True',
                    ),
                    ]
                ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),


        dcc.Graph(id="feature-graphic"),
        dash_table.DataTable(
              id='total-table-claves',
              columns=[
                        {"name": "Indicador", "id": "Indicador"},
                        {"name": "Total", "id": "Total"},
                      ],
              editable=True,
              # sorting=True,
              # sorting_type="multi",
              style_cell = {"fontFamily": "Muli", 'textAlign': 'left'},
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
        html.Div(
            [
            html.H6(
                ["Distribución tipo de producto"], className="subtitle padded"
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
            dcc.Graph(id="claves-medio-total"),
            html.H5(
                ["Distribución diária"], className="subtitle padded"
            ),
            dcc.Graph(id="claves-medio-dia"),
            ],className="six columns"
         ),
    ], style={'padding':10}

)

@app.callback(Output('dropdown-distritos', 'value'),
	[Input('items-options-distrito', 'value')])
def update_dropdown_distritos(option):
    if option == 'TODOS':
        return ['CUNDINAMARCA','ANTIOQUIA','REGION ANDINA','REGION ORINOQUIA','REGION CARIBE','REGION AMAZONICA','ATLANTICO','OTROS']
    else:
        return []

@app.callback(Output('total-table-claves', 'data'),
	[Input('my-date-picker-range-claves', 'start_date'),
	 Input('my-date-picker-range-claves', 'end_date')])
def update_data_1(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    data_total = filtered_df[["CLAVES","PUNTOS"]].sum().reset_index()
    data_total.columns = ["Indicador","Total"]
    data_total = data_total.to_dict("rows")
    return data_total

@app.callback(
    Output('feature-graphic', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun', 'value')])
def update_graph(start_date, end_date,column):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    month = int(df_claves_cat.DATE.max().month)
    filtered_df = filtered_df[filtered_df["MONTH"]==month].reset_index(drop=True)
    filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
    filtered_df = filtered_df.groupby(by=["YEAR","MONTH","DAY"])[column].sum().reset_index()
    filtered_df["DAY"] = filtered_df["MONTH"] + "-" + filtered_df["DAY"].astype(str)
    #Agregando graficas para cada año
    years = list(set(filtered_df["YEAR"]))
    n = len(years)
    data = []
    for i in range(n):
    	trace = go.Scatter(
    			x = filtered_df[filtered_df["YEAR"]==years[i]]["DAY"],
    	        y = filtered_df[filtered_df["YEAR"]==years[i]][column],

    	        name = str(years[i]),
    	        mode = 'lines+markers+text',
    	        # text = df[df["YEAR"]==year][column],
    	        textposition='middle center',
    	        textfont=  dict(
    	                         size=12,
    	                    ),
    	        marker = dict(
    	                        size = 5, color = colors[i],
    	                        line = dict(width = 2,)
    	                 )
    	    )
    	data.append(trace)

    layout = go.Layout(
            dict(
                title = "",
                plot_bgcolor  = "rgb(243,243,243)",
                paper_bgcolor = "rgb(243,243,243)",
                height=500 ,
                width=950,
                showlegend=True,
                legend={"x": -0.0277108433735,
                "y": -0.142606516291,
                "orientation": "h",
            })
    )

    return {
        "data": data,
        "layout": layout
    }

def update_graph_pie(df,column):
    df = df.groupby(by=['DISTRITO'])[column].sum().reset_index()
    trace = go.Pie(
                    values  = df[column].tolist(),
                    labels  = df['DISTRITO'].tolist(),
                    hoverinfo = "label+percent+value",
                    marker  = dict(line = dict(width = 2,
                                               color = "rgb(243,243,243)")
                                  ),
                    text= df[column].tolist(),
                    domain  = dict(x = [0,1]),
                    hole    = .5,
            )

    layout = go.Layout(dict(
                                title = "",
                                plot_bgcolor  = "rgb(243,243,243)",
                                paper_bgcolor = "rgb(243,243,243)",
                                annotations = [
                                                dict(
                                                        text = "Distrito",
                                                        font = dict(size = 13),
                                                        showarrow = False,
                                                        x = .5, y = .5
                                                ),
                                                ],
                              )
                )

    return {
        "data": [trace],
        "layout": layout
    }

#### Update graph mensual Callback
@app.callback(
    Output('claves-distrito', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun-distrito', 'value'),
     Input('dropdown-distritos', 'value')])
def update_graph_mes(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    return update_graph_pie(df=filtered_df,column=column)

#### Update graph distritos Callback
@app.callback(
    Output('claves-medio-total', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun-TipoPro', 'value'),
     Input('dropdown-distritos', 'value')])
def update_graph_distrito(start_date, end_date,column,distritos):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df_claves_cat[df_claves_cat.FECHA.between(dt.strftime(start_date, "%Y-%m-%d"),dt.strftime(end_date, "%Y-%m-%d"))]
    filtered_df = filtered_df[filtered_df["DISTRITO"].isin(distritos)].reset_index(drop=True)
    filtered_df['CATEGORIAS'] = filtered_df['CATEGORIAS'].map(cat_direc)
    df_clav_tipo_pro = filtered_df.groupby(by="CATEGORIAS")["CLAVES","PUNTOS"].sum().reset_index()
    trace = go.Pie(
                    values  = df_clav_tipo_pro[column].tolist(),
                    labels  = df_clav_tipo_pro['CATEGORIAS'].tolist(),
                    hoverinfo = "label+percent+value",
                    marker  = dict(line = dict(width = 2,
                                               color = "rgb(243,243,243)")
                                  ),
                    text= df_clav_tipo_pro[column].tolist(),
                    domain  = dict(x = [0,1]),
                    hole    = .5,
                )
    layout = go.Layout(dict(
                    title = "",
                    plot_bgcolor  = "rgb(243,243,243)",
                    paper_bgcolor = "rgb(243,243,243)",
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

#### Update graph distritos Callback
@app.callback(
    Output('claves-medio-dia', 'figure'),
    [Input('my-date-picker-range-claves', 'start_date'),
     Input('my-date-picker-range-claves', 'end_date'),
     Input('items-options-clav_pun-TipoPro', 'value'),
     Input('dropdown-distritos', 'value')])
def update_graph_TipoPro(start_date, end_date,column,distritos):
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
    filtered_df = filtered_df.groupby(by=["MONTH","DAY","CATEGORIAS"])[column].sum().reset_index()
    filtered_df = filtered_df.sort_values(by="DAY")
    filtered_df["MONTH"] = filtered_df["MONTH"].map(string_months)
    filtered_df["DAY"] = filtered_df["MONTH"] + "-" + filtered_df["DAY"].astype(str)
    filtered_df = filtered_df[["DAY","CATEGORIAS",column]].reset_index(drop=True)

    categorias = list(set(filtered_df["CATEGORIAS"]))
    n = len(categorias)
    data = []
    x = filtered_df['DAY'].unique().tolist()
    for i in range(n):
        trace = go.Bar(
                            x = x,
                            y = filtered_df[filtered_df["CATEGORIAS"]==categorias[i]][column],
                            name = str(categorias[i]),
                        )
        data.append(trace)

    layout = go.Layout(dict(title = "",
                        plot_bgcolor  = "rgb(243,243,243)",
                        paper_bgcolor = "rgb(243,243,243)",
                        showlegend=True,
                        barmode='stack'
                     )
                  )


    return {
        "data": data,
        "layout": layout
    }

if __name__ == '__main__':
    app.run_server(debug=True)
