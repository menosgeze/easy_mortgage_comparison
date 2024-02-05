import argparse
from dash import Dash, html, dash_table
import pandas as pd
from computations import compute_monthly_payment  
from computations.constants import Period

# Initialize the app
app = Dash(__name__)

# Global Variables
PRINCIPAL = 500000
YEARLY_RATE = 0.05
DURATION = 180

# Initial Data to Populate
default_data = [
    compute_monthly_payment(
        principal=PRINCIPAL,
        yearly_rate=YEARLY_RATE,
        duration=DURATION,
        extra_payment=0,
        extra_payment_period=Period.MONTH,
        special_payment={},
        initial_escrow=300,
        escrow_growth_rate=0.02,
        escrow_period=Period.YEAR,
    ),
    compute_monthly_payment(
        principal=PRINCIPAL,
        yearly_rate=YEARLY_RATE,
        duration=DURATION,
        extra_payment=500,
        extra_payment_period=Period.MONTH,
        special_payment={12: 5000, 24: 5000},
        initial_escrow=300,
        escrow_growth_rate=0.02,
        escrow_period=Period.YEAR,
    )
]

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

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

if __name__ == '__main__':
    port = parse_terminal_arguments()
    app.run(debug=True, port=port)



