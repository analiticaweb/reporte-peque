import dash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/pequenin-reporte/')
server = app.server
app.config.suppress_callback_exceptions = True

#import dash_auth

#VALID_USERNAME_PASSWORD_PAIRS = [['username', 'password'],['pequeintus','peque2019+']]

#auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)
