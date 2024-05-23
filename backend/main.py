# main.py
from loan import Loan
from borrower import Borrower
from params import INTEREST_RATE_CUTS_DNB


def calculate_loan(
    initial_interest_rate, loan_amount, repayment_period_years, salaries, splits, names
):
    INTEREST_RATE_CUTS = (
        INTEREST_RATE_CUTS_DNB  # or set this dynamically based on inputs
    )

    borrowers = []
    for i in range(len(salaries)):
        borrowers.append(Borrower(salaries[i], splits[i], names[i]))

    loan = Loan(initial_interest_rate, loan_amount, repayment_period_years, borrowers)

    payment_details = []

    for month in range(1, loan.repayment_period_months + 1):
        if month in INTEREST_RATE_CUTS:
            loan.reduce_interest(0.0025)
        loan.down_payment()
        payment_details.append(
            {
                "month": month,
                "remaining_loan_amount": loan.remaining_loan_amount,
                "total_payment": sum(
                    round(borrower.get_monthly_payment()) for borrower in loan.borrowers
                ),
                "borrowers": [
                    {
                        "name": borrower.name,
                        "monthly_payment": round(borrower.get_monthly_payment()),
                        "principal_payment": round(borrower.get_principal_payment()),
                        "interest_cost": round(borrower.get_interest_cost()),
                        "effective_interest_rate": round(
                            borrower.get_effective_interest_rate()
                        ),
                        "effective_monthly_payment": round(
                            borrower.get_effective_monthly_payment()
                        ),
                    }
                    for borrower in loan.borrowers
                ],
            }
        )

    return {
        "payment_details": payment_details,
        "remaining_loan_amount": loan.remaining_loan_amount,
    }
