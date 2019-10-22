from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime
import plotly.graph_objs as go
from plotly import tools
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None

colors = ['#9079b7','#4179bd','#00a94f','#ffd200','#00a6cb','#0d5409','#d77233','#bdefdd','#efba7b']


######################## FOR GRAPHS  ########################

#Update scatter graphs
def update_graph_scatter(df,column,per):
    years = list(set(df["YEAR"]))
    n = len(years)
    data = []
    if per=='DAY':

        for i in range(n):
            trace = go.Scatter(
                    x = df[df["YEAR"]==years[i]][per].apply(lambda date: date.split('-')[1]),
                    y = df[df["YEAR"]==years[i]][column],

                    name = str(years[i]),
                    mode = 'lines+markers+text',
                    #text = df[df["YEAR"]==years[i]][column],
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
                    title = df[df["YEAR"]==years[0]][per].apply(lambda date: date.split('-')[0]).tolist()[0],
                    legend_bgcolor = "rgb(255,255,255)",
                    plot_bgcolor  = "rgb(255,255,255)",
                    paper_bgcolor = "rgb(255,255,255)",
                    showlegend=True,
                    margin=dict(t=50),

                )
        )

    else:
        for i in range(n):
            trace = go.Scatter(
                    x = df[df["YEAR"]==years[i]][per],
                    y = df[df["YEAR"]==years[i]][column],

                    name = str(years[i]),
                    mode = 'lines+markers+text',
                    text = df[df["YEAR"]==years[i]][column],
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

    return {
        "data": data,
        "layout": layout
    }

#Update pie graphs
def update_graph_pie(df,column):
    df = df.groupby(by=['DISTRITO'])[column].sum().reset_index()
    trace = go.Pie(
                    values  = df[column].tolist(),
                    labels  = df['DISTRITO'].tolist(),
                    hoverinfo = "label+percent+value",
                    marker  = dict(line = dict(width = 2,
                                               color = "rgb(243,243,243)")
                                  ),
                    #text= df[column].tolist(),
                    domain  = dict(x = [0,1]),
                    hole    = .5,
                    marker_colors=colors
            )

    layout = go.Layout(dict(
                                title = "",
                                legend_bgcolor = "rgb(255,255,255)",
                                plot_bgcolor  = "rgb(255,255,255)",
                                paper_bgcolor = "rgb(255,255,255)",
                                margin=dict(t=50),
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

def temp_var(df):
    df["DATE"] = pd.to_datetime(df["FECHA"])
    df["MONTH"] = df["DATE"].dt.month
    df["YEAR"] = df["DATE"].dt.year
    df["DAY"] = df["DATE"].dt.day
    return df
