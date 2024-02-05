import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def trace_pie_distribution(
    payments: pd.DataFrame,
    principal: str = 'monthly_principal',
    interest: str = 'monthly_interest', 
    escrow: str = 'escrow'
    n_period: int = 0
):
    """Traces the pie comparing how much the monthly payment
    goes to each category: `principal`, `interest`, `escrow`.

    Args:
        payments (pd.DataFrame): containing the history of expected payments.
            Must have cols: principal, interest, escrow.
        principal (str): column containing the monthly principal paid.
        interest (str): column containing the monthly interest paid.
        escrow (str): column containing the monthly escrow paid.
        n_period (int): index of the month to use as a sample.
    
    Returns:
        (go.Pie): pie trace of the distribution of the monthly sample payment.
    """

    values = [
        payments[escrow][n_period],
        payments[principal][n_period],
        payments[interst][n_period],
    ]

    return go.Pie(
        labels=['escrow', 'principal', 'interest'],
        values=values,
        text=[f'${value}' for value in values],
        hole=0.5
    )


def trace_timeseries_principal(
    payments: pd.DataFrame, 
    color: str = 'Red',
    principal: str = 'standing_principal',
    name: str = 'principal',
):
    """Traces the history of the standing principal.

    Args:
        payments (pd.DataFrame): containing the history of expected payments.
            Must have cols: principal, interest, escrow.
        color (str): valid color for this trace.
        principal (str): column containing the standing principal at every month.
        interest (str): column containing the monthly interest paid.
        name (str): name for this trace to be used in the legend.

    Returns:
        (go.Scatter): linear plot of the standing principal per month.
    """

    return go.Scatter(
        x=payments[principal].index,
        y=payments[principal],
        name=name,
        mode='lines+markers',
        marker={'size': 1, 'color': color}
    )

def generate_default_graph(
    payments0: pd.DataFrame,
    payments1: pd.DataFrame,
    output_file: str = "Default",
    n_period: int = 0
):
    """Puts together the comparison graph, and saves it into an html file.
    Args:
        payments0 (pd.DataFrame): one set of payments.
        payments1 (pd.DataFrame): another set of payments.
        output_file (str): filename where to save.
        n_period (int): index of the month sample for the payments distribution.

    """

    fig = make_subplots(
        rows=3, cols=2, 
        specs=[
            [{'type': 'domain'}, {'type': 'domain'}], 
            [{'rowspan': 2, 'colspan': 2}, None],
            [None, None]
        ],
        shared_xaxes=False,
        shared_yaxes=False,
        vertical_spacing=0.01,
        subplot_titles=(
            f'Distribution at {n_period}-th month',
            'Alternative',
            'Principal Advance',
            None, None, None
        )
    )

    first_pie = trace_pie_distribution(payments=payments1, n_period=n_period)
    fig.add_trace(first_pie, row=1, col=1)

    second_pie = trace_pie_distribution(payments=payments2, n_period=n_period)
    fig.add_trace(first_pie, row=1, col=2)

    first_principal = trace_timeseries_principal(payments=payments1, color='Red')
    fig.add_trace(first_principal, row=2, col=1)

    second_principal = trace_timeseries_principa2(payments=payments1, color='Red') 
    fig.add_trace(second_principal, row=2, col=1)

    fig.update_layout(
        title="Mortgage History Comparison",
        height=1200, width=1200
    )

    if not output_file.endswith('.html'):
        output_file += '.html'
    
    fig.write_html(output_file)
