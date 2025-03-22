from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pan = models.CharField(max_length=11, unique=True)
    ufid = models.CharField(max_length=10, unique=True, null=True, blank=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


# Bank Accounts Model
class BankAccount(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='bank_accounts')
    account_type = models.CharField(max_length=50)  # e.g., Savings, Current, PPF, etc.
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.account_type} - {self.bank_name}"


# Fixed Deposits
class FixedDeposit(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='fixed_deposits')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_years = models.IntegerField()
    bank = models.CharField(max_length=100)

    def __str__(self):
        return f"FD - {self.bank}"


# Demat Account
class DematAccount(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='demat_accounts')

    def __str__(self):
        return f"Demat Account for {self.user_profile.user.username}"


# Stocks
class Stock(models.Model):
    demat_account = models.ForeignKey(DematAccount, on_delete=models.CASCADE, related_name='stocks')
    company = models.CharField(max_length=100)
    shares = models.IntegerField()
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.company} - {self.shares} shares"


# Mutual Funds
class MutualFund(models.Model):
    demat_account = models.ForeignKey(DematAccount, on_delete=models.CASCADE, related_name='mutual_funds')
    fund_name = models.CharField(max_length=100)
    units = models.IntegerField()
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.fund_name} - {self.units} units"


# Credit Cards
class CreditCard(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='credit_cards')
    bank = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Credit Card - {self.bank}"


# Debit Cards
class DebitCard(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='debit_cards')
    bank = models.CharField(max_length=100)
    linked_account = models.CharField(max_length=50)

    def __str__(self):
        return f"Debit Card - {self.bank}"


# Assets
class Asset(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=100)  # e.g., car, bike, gadget, real estate
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.asset_type} - {self.value}"


# Debts and Liabilities
class Debt(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='debts')
    debt_type = models.CharField(max_length=100)  # e.g., home loan, car loan
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_years = models.IntegerField()
    bank = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.debt_type} - {self.bank}"


# Insurance
class Insurance(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='insurance')
    insurance_type = models.CharField(max_length=100)  # e.g., life, health, business
    coverage = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sum_assured = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    premium = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.insurance_type} Insurance"


# Retirement Accounts
class RetirementAccount(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='retirement_accounts')
    account_type = models.CharField(max_length=100)  # e.g., EPF, NPS
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    annual_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.account_type} - {self.balance}"
