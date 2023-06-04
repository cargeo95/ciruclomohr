from dash import Dash, html,dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Circulo de Mohr"),
    dbc.Row([
            dbc.Col([
                html.H2("Valores de entrada"),
                html.H5("Estamos usando la ecuación: τ = C'  + σ' tanθ"),
                html.Label("Ingrese por favor la cohesión:"),
                dbc.Input(id="cohesion", type="number", placeholder="4", min=0, max=100, step=1, value  = 0 ),
                html.Label("Ingrese por favor el ángulo de fricción:"),
                dbc.Input(id="angulo", type="number", placeholder="4", min=0, max=100, step=1, value = 29),
                html.Label("El suelo está a una profunidad de:"),
                dbc.Input(id="profundiad", type="number", placeholder="4", min=0, max=100, step=1, value = 2),
                html.Label("Se asume un K0 de: 0.5 y un gamma seco de 20kN/m3"),
                html.Label("El suelo sufre una sobre carga:"),
                dbc.Input(id="carga", type="number", placeholder="4", min=0, max=100, step=1, value = 0)
                ],
                md=6
            ),
            dbc.Col([
                html.H2("Gráfica"),
                html.Div(id="resultados")
                ],             
                md=6
            )
        ]),
    
    
    
])

@callback(
    Output("resultados", "children"),
    Input("cohesion", "value"),
    Input("angulo", "value"),
    Input("profundiad", "value"),
    Input("carga", "value")
)

def calculoT(cohesion, angulo, profundiad, carga):
    
    if cohesion is None or angulo is None or profundiad is None:
        return "Ingrese los valores por favor"
    
    cohesion = int(cohesion)
    angulo = int(angulo)
    profundiad = int(profundiad)
    carga = int(carga)
    
    sigma = np.linspace(profundiad * 20 * 0.5, profundiad * 20 + carga, 10)
    tao = cohesion + sigma * np.tan(angulo)
    
    sigma_1 = profundiad * 20 + carga
    sigma_3 = profundiad * 20 * 0.5
    radio = (sigma_1 - sigma_3)/2
    centro = (sigma_1 + sigma_3)/2
    
    theta = np.linspace(0, np.pi, 100)  # Rango de ángulo de 0 a pi (mitad superior del círculo)
    x_values = centro + radio * np.cos(theta)
    y_values =  radio * np.sin(theta)


    
    return html.Div([     
        dcc.Graph(
            figure = go.Figure(
                data=[
                    go.Scatter(x=sigma, y=tao, mode='lines', name='Línea de falla'),
                    go.Scatter(x=x_values, y=y_values, mode='lines', name='Círculo'),
                    go.Scatter(x=[sigma_1], y = [0], mode='markers', name='Punto sigma1'),
                    go.Scatter(x=[sigma_3], y = [0], mode='markers', name='Punto sigma3'),
                ],
                layout=go.Layout(
                    title='Diagrama de Mohr',
                    xaxis=dict(title="σ' (kPa)"),
                    yaxis=dict(title="τ (kPa)"),
                    showlegend=True
                )
                                
            )
            
        )
    ])

if __name__ == "__main__":
    app.run_server(debug=True)
