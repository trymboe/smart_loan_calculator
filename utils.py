import matplotlib.pyplot as plt

from params import INTEREST_RATE_CUTS_DNB, TAX_PERCENT
from loan import Loan


def calculate_payment(initial_interest_rate, loan_amount, repayment_period_months):
    monthly_interest_rate = initial_interest_rate / 12
    factor = (1 + monthly_interest_rate) ** repayment_period_months
    monthly_payment = loan_amount * (monthly_interest_rate * factor) / (factor - 1)
    return monthly_interest_rate, monthly_payment


def calculate_tax_deduction(salary, intrest_cost_list):
    prev_tax_bracket = 50_000
    tax_bracket_list = []

    for tax_bracket in TAX_PERCENT:
        if salary < tax_bracket:
            current_tax_bracket = prev_tax_bracket
            break
        prev_tax_bracket = tax_bracket

    prev_tax_bracket = 50_000
    for intrest_cost in intrest_cost_list:
        for tax_bracket in TAX_PERCENT:
            if salary - intrest_cost < tax_bracket:
                tax_bracket_list.append((current_tax_bracket, prev_tax_bracket))
                break
            prev_tax_bracket = tax_bracket

    deduction_amount_list = []

    for i, [starting_tax_bracket, prev_tax_bracket] in enumerate(tax_bracket_list):

        running_tax_bracket = starting_tax_bracket
        running_salary = salary
        deduction_amount = 0
        current_deducted_amount = 0
        while True:
            deduction_caluclation_value = running_salary - running_tax_bracket
            if (
                current_deducted_amount + deduction_caluclation_value
                > intrest_cost_list[i]
            ):
                deduction_caluclation_value = (
                    intrest_cost_list[i] - current_deducted_amount
                )
            current_deducted_amount += deduction_caluclation_value
            running_salary = salary - deduction_caluclation_value
            deduction_amount += (
                deduction_caluclation_value * TAX_PERCENT[running_tax_bracket]
            )

            next_index = list(TAX_PERCENT.keys()).index(running_tax_bracket) - 1
            next_tax_bracket = list(TAX_PERCENT.keys())[next_index]
            if next_tax_bracket < prev_tax_bracket:
                break
            running_tax_bracket = next_tax_bracket

        deduction_amount_list.append(deduction_amount)

    return deduction_amount_list


def annuity_loan_calculation(loan: Loan, salary):

    for month in range(1, loan.repayment_period_months + 1):
        if month in INTEREST_RATE_CUTS_DNB:
            loan.reduce_interest(0.0025)
        if month % 12 == 0:
            for borrower in loan.borrowers:
                borrower.increase_salary()

        loan.down_payment()

    # tax_deduction_list = calculate_tax_deduction(salary, interest_cost_list)


def plot_loan(interest_cost_list, principal_payment_list):
    plt.plot(interest_cost_list, label="Interest Cost")
    plt.plot(principal_payment_list, label="Principal Payment")
    plt.legend()
    plt.show()


def print_loan(
    loan_balance_list,
    interest_cost_list,
    effective_interest_cost_list,
    principal_payment_list,
    monthly_payment_list,
    effective_monthly_payment_list,
    tax_deduction_list,
):
    for i in range(len(loan_balance_list)):
        print(
            f"Month: {i+1}, Remaining Loan: {loan_balance_list[i]:.2f}, Principal Payment: {principal_payment_list[i]:.2f}, Interest Cost: {interest_cost_list[i]:.2f}, Effective Interest Cost: {effective_interest_cost_list[i]:.2f}, Monthly Payment: {monthly_payment_list[i]:.2f}, Effective Monthly Payment: {effective_monthly_payment_list[i]:.2f}, Tax deduction: {tax_deduction_list[i]:.2f}"
        )
        print()
