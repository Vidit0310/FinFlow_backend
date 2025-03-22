from django.contrib import admin
from .models import UserProfile,BankAccount, FixedDeposit, DematAccount, Stock, MutualFund, CreditCard, DebitCard, Asset, Debt, Insurance, RetirementAccount
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(BankAccount)
admin.site.register(FixedDeposit)
admin.site.register(DematAccount)
admin.site.register(Stock)
admin.site.register(MutualFund)
admin.site.register(CreditCard)
admin.site.register(DebitCard)
admin.site.register(Asset)
admin.site.register(Debt)
admin.site.register(Insurance)
admin.site.register(RetirementAccount)