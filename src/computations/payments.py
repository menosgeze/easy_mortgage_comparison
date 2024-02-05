from __future__ import annotations
import numpy as np
import pandas as pd
from .constants import Period


def compute_raw_payments(
    principal: float,
    yearly_rate: float = 0.0225,
    duration: int = 180,
    extra_payment: float = 0.0,
    extra_payment_period: Period = Period.MONTH,
    special_payment: dict = dict()
) -> pd.DataFrame:
    """
    Args:
        principal (float): money initially borrowed or still owed to the bank.
        yearly_rate (float): mortgage rate.
        duration (float): duration in months, e.g. 15 years is 180 months.
    """
    monthly_rate = (1 + yearly_rate) ** (1 / 12) - 1
    final_rate_factor = (1 + monthly_rate) ** duration
    monthly_payment = (
        principal * monthly_rate * final_rate_factor / (final_rate_factor - 1)
    )

    final_rate_factor = (1 + monthly_rate) ** duration
    monthly_payment = np.round(
        (principal * monthly_rate * final_rate_factor / (final_rate_factor - 1)), 2
    )

    monthly_data = []
    remaining_principal = principal

    while duration > 0 and remaining_principal > 0:
        month_interest = np.round(remaining_principal * monthly_rate, 2)
        month_principal = np.round(monthly_payment - month_interest, 2)
        if remaining_principal <= month_principal:
            month_principal = np.round(remaining_principal, 2) + 0.01

        remaining_principal -= month_principal

        if (len(monthly_data) + 1) % extra_payment_period.value == 0:
            remaining_principal -= extra_payment

        if len(monthly_data) in special_payment:
            remaining_principal -= special_payment[len(monthly_data)]

        remaining_principal = np.round(remaining_principal, 2)
        duration -= 1

        monthly_data.append((
            duration,
            remaining_principal,
            month_interest,
            month_principal,
        ))

    return pd.DataFrame(
        monthly_data,
        columns=[
          "n_months_remaining",
          "standing_principal",
          "monthly_interest_expense",
          "monthly_principal_expense",
        ],
    ).reset_index(names="month_number")

def computing_monthly_escrow(
    initial_escrow: float,
    escrow_growth_rate: float = 0.01,
    escrow_period: Period = Period.YEAR,
    duration: int = 180
):
    """Computes the monthly escrow into a series of shape
    `duration` * 12.

    Args:
        initial_escrow (float): escrow to be paid the first period.
        escrow_growth_rate (float): increase rate of the escrow.
        escrow_period (Period): whether the escrow is going to increase
            every year, half of a year, trimester, or monthly.
        duration (int): number of months of the transaction.

    Returns:
        (np.array): of shape `duration` representing the monthly escrow
            to pay during the transaction.
    """
    escrow_series = initial_escrow * np.array([
        [(1 + escrow_growth_rate) ** this_period for _ in range(escrow_period.value)] 
        for this_period in np.arange(duration / escrow_period.value)
    ]).flatten()

    return np.round(escrow_series, 2)


def compute_monthly_payment(
    principal: float,
    yearly_rate: float = 0.0225,
    duration: int = 180,
    extra_payment: float = 0.0,
    extra_payment_period: Period = Period.MONTH,
    special_payment: dict = dict(),
    initial_escrow: float=200,
    escrow_growth_rate: float = 0.01,
    escrow_period: Period = Period.YEAR,
):
    payments = compute_raw_payments(
        principal,
        yearly_rate,
        duration,
        extra_payment,
        extra_payment_period,
        special_payment
    )

    payments['escrow'] = computing_monthly_escrow(
        initial_escrow,
        escrow_growth_rate,
        escrow_period,
        duration
    )[: len(payments)]

    return payments


if __name__ == '__main__':
    print("This is a sample result:")
    pd.options.display.max_columns = 10

    payments = compute_monthly_payment(
        principal=140000,
        yearly_rate=0.0225,
        duration=180,
        extra_payment=50,
        extra_payment_period=Period.MONTH,
        special_payment={
            12: 5000,
            24: 5000
        },
        initial_escrow=160,
        escrow_growth_rate=0.01,
        escrow_period=Period.YEAR,
    )

    print(payments.head(5))

    print('...')

    print(payments.tail(5))
