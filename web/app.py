# A demo app to work out how to do the following
# Stop one callback blocking another callback by handing the work off to a celery queue
# Keep the cache warm by using celery beat

import requests
import orjson
import dash
import dash_mantine_components as dmc
from dash import CeleryManager, Input, Output, callback
from flask import Flask

from web.config import get_settings
from web.celery import redis_client
from web.tasks import get_response


server = Flask(__name__)

# Set up fast and slow requests for testing
slow_url = "http://127.0.0.1:8101/ping/slow"
fast_url = "http://127.0.0.1:8101/ping/fast"


@dash.callback(
    Output("ping-fast-text", "children"),
    [Input("ping-fast-button", "n_clicks")],
    prevent_initial_call=True,
)
def ping_fast(n_clicks):
    response = requests.get(fast_url)
    data = response.json()
    return f"Click: {n_clicks} Timestamp: {data}"


@dash.callback(
    Output("ping-slow-text", "children"),
    [Input("ping-slow-button", "n_clicks")],
    prevent_initial_call=True,
)
def ping_slow(n_clicks):
    # check the redis cache for the data
    cache_key = "slow_url"
    cached_data = redis_client.get(cache_key)

    if cached_data is None:
        fetch_data_task = get_response.delay(slow_url, cache_key)
        data = fetch_data_task.get()
    else:
        data = orjson.loads(cached_data)

    return f"Click: {n_clicks} Timestamp: {data}"


layout = dmc.Paper(
    [
        dmc.Title("Hello World"),
        dmc.Group(
            [
                dmc.Button(id="ping-fast-button", children="Ping-fast"),
                dmc.Text(id="ping-fast-text"),
            ],
            p=10,
        ),
        dmc.Group(
            [
                dmc.Button(id="ping-slow-button", children="Ping-slow"),
                dmc.Text(id="ping-slow-text"),
            ],
            p=10,
        ),
    ]
)


app = dash.Dash(
    __name__,
    server=server,
)

app.layout = layout
app.config.suppress_callback_exceptions = True

# set debug UI settings on/off when running under gunicorn
if get_settings().debug:
    app.enable_dev_tools(dev_tools_ui=True, dev_tools_hot_reload=False)

# expose application's object server so wsgi server can access it
server = app.server

if __name__ == "__main__":
    debug = True if get_settings().debug else False
    app.run_server(host="0.0.0.0", port=8100, debug=debug)
