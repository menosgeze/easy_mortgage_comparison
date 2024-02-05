import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def trace_pie_distribution(
    payments: pd.DataFrame,
    principal: str = "monthly_principal",
    interest: str = "monthly_interest",
    escrow: str = "escrow",
    n_period: int = 0,
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
        payments[interest][n_period],
    ]

    return go.Pie(
        labels=["escrow", "principal", "interest"],
        values=values,
        text=[f"${value}" for value in values],
        hole=0.5,
    )


def trace_timeseries(
    payments: pd.DataFrame,
    color: str = "Red",
    principal: str = "standing_principal",
    name: str = "principal",
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
        x=[val/12 for val in payments[principal].index],
        y=payments[principal],
        name=name,
        mode="lines+markers",
        marker={"size": 1, "color": color},
    )


def generated_annotated_point(
    x_value: float,
    y_value: float,
    name: str,
    text: str,
    color: str,
):
    """Generates an annotated point.

    Args:
        x_value (float): x-coordinate,
        y_value (float): y-coordinate,
        name (str): name of the point in the legend.
        text (str): text to display.
        color (str): color of the point.

    Returns:
        (go.Scatter): trace of a single annotated point.
    """
    return go.Scatter(
        x=[x_value],
        y=[y_value],
        name=name,
        text=text,
        mode="markers+text",
        marker={"color": color},
        textposition="bottom left",
    )


def generate_default_graph(
    payments1: pd.DataFrame, payments2: pd.DataFrame, n_period: int = 0
):
    """Puts together the comparison graph, and saves it into an html file.
    Args:
        payments1 (pd.DataFrame): one set of payments.
        payments2 (pd.DataFrame): another set of payments.
        n_period (int): index of the month sample for the payments distribution.

    """
    fig = make_subplots(
        rows=2, cols=2, 
        specs=[
            [{'type': 'domain'}, {'type': 'domain'}], 
            [{}, {}]
        ],
        shared_xaxes=False,
        shared_yaxes=False,
        vertical_spacing=0.01,
        subplot_titles=(
            f'Distribution at {n_period}-th month',
            'Alternative Distribution',
            'Principal Advance',
            'Accumulated Interest Paid'
        )
    )

    first_pie = trace_pie_distribution(payments=payments1, n_period=n_period)

    fig.add_trace(first_pie, row=1, col=1)

    second_pie = trace_pie_distribution(payments=payments2, n_period=n_period)

    fig.add_trace(second_pie, row=1, col=2)

    first_principal = trace_timeseries(
        payments=payments1, color="Red", name="principal"
    )

    fig.add_trace(first_principal, row=2, col=1)

    second_principal = trace_timeseries(
        payments=payments2, color="DarkRed", name="alt. principal"
    )
    fig.add_trace(second_principal, row=2, col=1)

    first_acc_interest = trace_timeseries(
        payments1, color="Blue", principal="acc_interest", name="interest"
    )
    fig.add_trace(first_acc_interest, row=2, col=2)

    x_value = payments1.index[-1] / 12
    years = int((x_value + 1) / 12)
    months = (x_value + 1) % 12
    y_value = np.round(payments1["acc_interest"].max(), 2)
    text = f"${y_value} in {years}y {months}m"
    ending_interest1 = generated_annotated_point(
        x_value=x_value, y_value=y_value, name="", text=text, color="Blue"
    )
    fig.add_trace(ending_interest1, row=2, col=2)


    second_acc_interest = trace_timeseries(
        payments2, color="DarkBlue", principal="acc_interest", name="alt. interest"
    )
    fig.add_trace(second_acc_interest, row=2, col=2)

    x_value = payments2.index[-1] / 12
    years = int((x_value + 1) / 12)
    months = (x_value + 1) % 12
    y_value = np.round(payments2["acc_interest"].max(), 2)
    text = f"${y_value} in {years}y {months}m"
    ending_interest2 = generated_annotated_point(
        x_value=x_value, y_value=y_value, name="", text=text, color="DarkBlue"
    )
    fig.add_trace(ending_interest2, row=2, col=2)

    fig.update_layout(title="Mortgage History Comparison", height=800, width=800) # , showlegend=False)

    return fig
