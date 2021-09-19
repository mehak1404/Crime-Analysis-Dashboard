import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
# from sklearn import datasets
# from sklearn.cluster import KMeans

# crime_raw = datasets.load_crime()
# crime = pd.DataFrame(crime_raw["data"], columns=crime_raw["feature_names"])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Select District"),
                dcc.Dropdown(
                    id="x-variable",
                    # options=[
                    #     {"label": col, "value": col} #for col in crime.columns
                    # ],
                    value="District",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Select Type of Crime"),
                dcc.Dropdown(
                    id="y-variable",
                    # options=[
                    #     {"label": col, "value": col} #for col in crime.columns
                    # ],
                    value="Crimetype",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Select Year"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Crime Analysis Dashboard"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


# @app.callback(
#     Output("cluster-graph", "figure"),
#     [
#         Input("x-variable", "value"),
#         Input("y-variable", "value"),
#         Input("cluster-count", "value"),
#     ],
# )
# def make_graph(x, y, n_clusters):
#     # minimal input validation, make sure there's at least one cluster
#     km = KMeans(n_clusters=max(n_clusters, 1))
#     df = crime.loc[:, [x, y]]
#     km.fit(df.values)
#     df["cluster"] = km.labels_

#     centers = km.cluster_centers_

#     data = [
#         go.Scatter(
#             x=df.loc[df.cluster == c, x],
#             y=df.loc[df.cluster == c, y],
#             mode="markers",
#             marker={"size": 8},
#             name="Cluster {}".format(c),
#         )
#         for c in range(n_clusters)
#     ]

#     data.append(
#         go.Scatter(
#             x=centers[:, 0],
#             y=centers[:, 1],
#             mode="markers",
#             marker={"color": "#000", "size": 12, "symbol": "diamond"},
#             name="Cluster centers",
#         )
#     )

#     layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}

#     return go.Figure(data=data, layout=layout)


# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option v"""
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in crime.columns
    ]


# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
    filter_options
)
app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
    filter_options
)


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)