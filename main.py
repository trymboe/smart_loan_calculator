import matplotlib.pyplot as plt
from loan import Loan
from borrower import Borrower

from params import INTEREST_RATE_CUTS_DNB


def main():

    # Loan parameters
    initial_interest_rate = 0.0544
    loan_amount = 5_000_000
    repayment_period_years = 30

    # Borrower parameters
    salary = [1_000_000, 1_000_000]
    split = [0.5, 0.5]
    name = ["Borrower 1", "Borrower 2"]

    borrowers = []
    for i in range(len(salary)):
        borrowers.append(Borrower(salary[i], split[i], name[i]))

    loan = Loan(initial_interest_rate, loan_amount, repayment_period_years, borrowers)

    for month in range(1, loan.repayment_period_months + 1):

        if month in INTEREST_RATE_CUTS_DNB:
            loan.reduce_interest(0.0025)

        loan.down_payment()

    # plot_loan(interest_cost_list, principal_payment_list)
    # print_loan(
    #     loan_balance_list,
    #     interest_cost_list,
    #     effective_interest_cost_list,
    #     principal_payment_list,
    #     monthly_payment_list,
    #     effective_monthly_payment_list,
    #     tax_deduction_list,
    # )


if __name__ == "__main__":
    main()
