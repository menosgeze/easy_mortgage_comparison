import argparse
import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd
from computations import compute_monthly_payment  
from computations.constants import Period
from plotting import generate_default_graph   
import dash_bootstrap_components as dbc

# Initialize the app
# Global Variables
PRINCIPAL = 500000
YEARLY_RATE = 0.05
DURATION = 180
PERIOD = {1: Period.MONTH, 3: Period.TRIMESTER, 6: Period.HALF_YEAR, 12: Period.YEAR}

app = Dash(__name__)
app.title = "Easy Mortgage Compare"
app.layout = html.Div([ 
    html.H1('Settings'),
    html.P('Please enter the expected escrow: '), 
    html.Div([
        dcc.Input(id="escrow", type="number", placeholder="Initial Escrow"),
        dcc.Input(id="escrow_growth_rate", type="number", placeholder="Escrow Growth Rate"),
        dcc.Input(id="escrow_period", type="number", placeholder="Escrow Growth Period"),
    ]),

    html.P('Please enter the first scenario: '),
    html.Div([
        dcc.Input(id="principal", type="number", placeholder="Amount Borrowed"),
        dcc.Input(id="yearly_rate", type="number", placeholder="Mortgage Rate"),
        dcc.Input(id="duration", type="number", placeholder="Duration in Months"),
        dcc.Input(id="extra_payement", type="number", placeholder="Regular Extra Payments"), 
        dcc.Input(id="extra_period", type="number", placeholder="How Often in months"),  
    ]),
          
    html.P('Please enter the second scenario: '),
    html.Div([
        dcc.Input(id="alt_principal", type="number", placeholder="Amount Borrowed"),
        dcc.Input(id="alt_yearly_rate", type="number", placeholder="Mortgage Rate"),
        dcc.Input(id="alt_duration", type="number", placeholder="Duration in Months"),
        dcc.Input(id="alt_extra_payement", type="number", placeholder="Regular Extra Payments"),
        dcc.Input(id="alt_extra_period", type="number", placeholder="How Often in Months"), 
    ]),
    dcc.Graph(figure=None, id="graph")
])

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [
        dash.dependencies.Input('escrow', 'value'),
        dash.dependencies.Input('escrow_growth', 'value'),
        dash.dependencies.Input('escrow_period', 'value'),
        dash.dependencies.Input('principal', 'value'),
        dash.dependencies.Input('yearly_rate', 'value'),
        dash.dependencies.Input('duration', 'value'),
        dash.dependencies.Input('extra_payment', 'value'),
        dash.dependencies.Input('extra_period', 'value'),
        dash.dependencies.Input('alt_principal', 'value'),
        dash.dependencies.Input('alt_yearly_rate', 'value'),
        dash.dependencies.Input('alt_duration', 'value'),
        dash.dependencies.Input('alt_extra_payment', 'value'),
        dash.dependencies.Input('alt_extra_period', 'value'),
    ]
)
def update_output(
    escrow,
    escrow_growth,
    escrow_period, 
    principal,
    yearly_rate,
    duration, 
    extra_payment,
    extra_period,
    alt_principal,
    alt_yearly_rate,
    alt_duration, 
    alt_extra_payement,
    alt_extra_period,

):

    if escrow_period not in [1, 3, 6, 12]:
        raise ValueError(
            f'Escrow Growth Period {escrow_period} must be 1, 3, 6, or 12'
        )

    if extra_period not in [1, 3, 6, 12]:
        raise ValueError(
            f'How often extra payments are {extra_period} must be 1, 3, 6, or 12'
        )
    if alt_extra_period not in [1, 3, 6, 12]:
        raise ValueError(
            f'How often extra payments are {alt_extra_period} must be 1, 3, 6, or 12'
        )

    payments1 = compute_monthly_payment(
        principal=principal,
        yearly_rate=yearly_rate,
        duration=duration,
        extra_payment=extra_payment,
        extra_payment_period=PERIOD[extra_period],
        special_payment={},
        initial_escrow=escrow,
        escrow_growth_rate=escrow_growth,
        escrow_period=PERIOD[escrow_period],
    )
    payments2 = compute_monthly_payment(
        principal=alt_principal,
        yearly_rate=alt_yearly_rate,
        duration=alt_duration,
        extra_payment=alt_extra_payment,
        extra_payment_period=PERIOD[alt_extra_period],
        special_payment={},
        initial_escrow=escrow,
        escrow_growth_rate=escrow_growth,
        escrow_period=PERIOD[escrow_period],
    )
    fig = generate_default_graph(payments0, payments1)
    return fig 

def parse_terminal_arguments() -> int:
    """Parses the terminal argument for a custom port.

    Returns:
        (int): Port to run the app. Default to 8050.
    """
    parser = argparse.ArgumentParser(
        prog='easy_mortgage_comparison',
        description='Parses the port to run the app.',
        epilog='The port must be between 1 and 2 ** 16 - 1 or 65535.'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=8050, help="Port numbers must be between 1 and 65535."
    )
    args = parser.parse_args()
    
    return args.port


if __name__ == '__main__':
    port = parse_terminal_arguments()
    app.run(debug=True, port=port)

