class Borrower:
    def __init__(self, salary, loan_percentage, name):
        self.salary = salary
        self.loan_percentage = loan_percentage

        self.monthly_payments = []
        self.tax_deductions = []
        self.principal_payments = []
        self.interest_cost = []
        self.name = name

    def __str__(self):
        return f"salary: {self.salary}, loan_percentage: {self.loan_percentage}, name: {self.name}"

    def add_tax_deduction(self, tax_deduction):
        self.tax_deductions.append(tax_deduction)

    def add_monthly_payment(self, monthly_payment):
        self.monthly_payments.append(monthly_payment)

    def add_interest_cost(self, interest_cost):
        self.interest_cost.append(interest_cost)

    def get_interest_cost(self):
        return self.interest_cost[-1]

    def get_effective_monthly_payment(self):
        return self.monthly_payments[-1] - self.tax_deductions[-1]

    def get_effective_interest_rate(self):
        return self.interest_cost[-1] - self.tax_deductions[-1]

    def add_monthly_interest_rate(self, monthly_interest_rate):
        self.monthly_interest_rates.append(monthly_interest_rate)

    def get_monthly_payment(self):
        return self.monthly_payments[-1]

    def get_salary(self):
        return self.salary

    def add_principal_payment(self, principal_payment):
        self.principal_payments.append(principal_payment)

    def get_principal_payment(self):
        return self.principal_payments[-1]
