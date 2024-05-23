from params import INTEREST_RATE_CUTS_DNB, TAX_PERCENT


class Loan:
    def __init__(self, interest_rate, loan_amount, repayment_period_years, borrowers):

        self.interest_rate = round(interest_rate, 4)
        self.loan_amount = loan_amount
        self.remaining_loan_amount = loan_amount
        self.repayment_period_years = repayment_period_years

        self.repayment_period_months = repayment_period_years * 12
        self.borrowers = borrowers

        for borrower in self.borrowers:
            self.calculate_payment(borrower)

    def __str__(self):
        return f"remaining_loan_amount: {round(self.remaining_loan_amount)}, borrowers: {self.borrowers}, repayment_period_years: {self.repayment_period_years}"

    def print_this_payment(self):
        total_payment = 0
        for borrower in self.borrowers:
            total_payment += borrower.get_monthly_payment()

        print(
            f"Måned {self.repayment_period_years * 12 - self.repayment_period_months} - Restgjeld: {round(self.remaining_loan_amount)} - Terminbeløp denne måneden: {round(total_payment)} - Gjeldende rente: {round(self.interest_rate * 100,2)}%"
        )
        for borrower in self.borrowers:
            print(
                f"{borrower.name:<10} - Terminbeløp: {round(borrower.get_monthly_payment()):<6}, Avdrag: {round(borrower.get_principal_payment()):<6}, Renter: {round(borrower.get_interest_cost()):<6}, effektiv rente: {round(borrower.get_effective_interest_rate()):<6}, effektivt terminbeløp: {round(borrower.get_effective_monthly_payment()):<6}"
            )
        print()

    def calculate_payment(self, borrower):
        loan_amount = self.remaining_loan_amount * borrower.loan_percentage

        monthly_interest_rate = round(self.interest_rate / 12, 4)
        factor = (1 + monthly_interest_rate) ** self.repayment_period_months
        monthly_payment = loan_amount * (monthly_interest_rate * factor) / (factor - 1)

        borrower.add_monthly_payment(monthly_payment)
        self.monthly_interest_rate = monthly_interest_rate

    def reduce_interest(self, reduction):
        self.interest_rate -= reduction
        self.interest_rate = round(self.interest_rate, 4)
        for borrower in self.borrowers:
            self.calculate_payment(borrower)

    def get_interest_cost(self, borrower):
        return (
            self.remaining_loan_amount
            * self.monthly_interest_rate
            * borrower.loan_percentage
        )

    def get_principal_payment(self, borrower):
        return borrower.get_monthly_payment() - self.get_interest_cost(borrower)

    def get_tax_deduction(self, borrower):
        return self.calculate_tax_deduction(
            borrower.get_salary(), self.get_interest_cost(borrower)
        )

    def down_payment(self):
        self.repayment_period_months -= 1
        down_payments = 0
        for borrower in self.borrowers:
            down_payments += self.get_principal_payment(borrower)

        if down_payments > self.remaining_loan_amount:
            down_payments = self.remaining_loan_amount
            borrower.add_principal_payment(down_payments)
            borrower.add_interest_cost(self.get_interest_cost(borrower))
            borrower.add_tax_deduction(self.get_tax_deduction(borrower))

        for borrower in self.borrowers:
            borrower.add_principal_payment(self.get_principal_payment(borrower))
            borrower.add_interest_cost(self.get_interest_cost(borrower))
            borrower.add_tax_deduction(self.get_tax_deduction(borrower))
        self.remaining_loan_amount -= down_payments
        self.print_this_payment()

    def calculate_tax_deduction(self, salary, intrest_cost):
        prev_tax_bracket = 50_000
        current_tax_bracket = 0
        final_tax_bracket = 0

        for tax_bracket in TAX_PERCENT:
            if salary < tax_bracket:
                current_tax_bracket = prev_tax_bracket
                break
            prev_tax_bracket = tax_bracket

        prev_tax_bracket = 50_000

        deduction_amount_list = []

        running_salary = salary
        deduction_amount = 0
        current_deducted_amount = 0
        final = False
        while True:
            deduction_caluclation_value = running_salary - current_tax_bracket
            if current_deducted_amount + deduction_caluclation_value > intrest_cost:
                deduction_caluclation_value = intrest_cost - current_deducted_amount
                final = True
            current_deducted_amount += deduction_caluclation_value
            running_salary = salary - deduction_caluclation_value
            deduction_amount += (
                deduction_caluclation_value * TAX_PERCENT[current_tax_bracket]
            )

            next_index = list(TAX_PERCENT.keys()).index(current_tax_bracket) - 1
            next_tax_bracket = list(TAX_PERCENT.keys())[next_index]
            if final:
                break
            current_tax_bracket = next_tax_bracket

        return deduction_amount
