import dash


app = dash.Dash(__name__, url_base_pathname='/raporty/', external_stylesheets="/assets/styles.css")
server = app.server
app.config.suppress_callback_exceptions = True
