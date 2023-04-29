from dash import Dash, html, Input, Output
from time import sleep

app = Dash()
app.layout = html.Div([
    html.Button("Fast", id="btn_fast"),
    html.Button("Slow", id="btn_slow"),
    html.Div(id="log_fast"),
    html.Div(id="log_slow")
])
server = app.server


@app.callback(Output("log_fast", "children"), Input("btn_fast", "n_clicks"))
def update1(n_clicks):
    return f"You clicked {n_clicks} times on the fast button."


@app.callback(Output("log_slow", "children"), Input("btn_slow", "n_clicks"))
def update1(n_clicks):
    sleep(5)
    return f"You clicked {n_clicks} times on the slow button."