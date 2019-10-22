import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from app import server
from app import app
from layouts import (
                    layout_Registros,
                    layout_Claves,
                    layout_Redenciones,
                    layout_Trafico
                    )
import callbacks
#this is a comment to git push and deploy again
import pandas as pd
import io
from flask import send_file

# see https://dash.plot.ly/external-resources to alter header, footer and favicon

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/pequenin-reporte/registros-hist":
        return layout_Registros
    elif pathname == "/pequenin-reporte/claves-hist":
        return layout_Claves
    elif pathname == "/pequenin-reporte/redenciones-hist":
        return layout_Redenciones
    elif pathname == "/pequenin-reporte/trafico-hist":
        return layout_Trafico
    else:
        return layout_Registros

if __name__ == '__main__':
    app.run_server(debug=True)
