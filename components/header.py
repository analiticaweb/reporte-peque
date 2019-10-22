import dash_html_components as html
import dash_core_components as dcc
from app import app

def Header():
    return html.Div(
                [
                    get_header(),
                    html.Br([]),
                    get_menu()
                ],style={"margin": "auto"}
            )


def get_header():
    header = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("tablero-gerencial.png"),
                        className="logo",
                    )
                ],
                className="row contentTitel",
            )
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Registros y activos",
                href="/pequenin-reporte/registros-hist",
                className="tab first",
            ),
            dcc.Link(
                "Ingreso de claves",
                href="/pequenin-reporte/claves-hist",
                className="tab",
            ),
            dcc.Link(
                "Redenciones",
                href="/pequenin-reporte/redenciones-hist",
                className="tab",
            ),
            dcc.Link(
                "Métricas del portal",
                href="/pequenin-reporte/trafico-hist",
                className="tab"
            ),

        ],
        className="row all-tabs",
    )
    return menu

def print_button():
    printButton = html.A(['Print PDF'],className="button no-print print",style={'position': "absolute", 'top': '-40', 'right': '0'})
    return printButton

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='https://i.pinimg.com/564x/4a/bc/38/4abc38758eba60d6712bd86dd1542697.jpg', height='101', width='141')
        ], className="ten columns padded"),

        # html.Div([
        #     dcc.Link('Full View   ', href='/cc-travel-report/full-view')
        # ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo
