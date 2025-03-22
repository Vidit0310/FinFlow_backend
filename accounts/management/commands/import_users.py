import json
import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import (
    UserProfile, BankAccount, DematAccount, Stock, MutualFund,
    CreditCard, DebitCard, Asset, Debt, Insurance, RetirementAccount
)
from django.db import transaction


# ✅ Function to generate random PAN
def generate_random_pan():
    return (
        ''.join(random.choices(string.ascii_uppercase, k=5)) +
        ''.join(random.choices(string.digits, k=4)) +
        random.choice(string.ascii_uppercase)
    )


# ✅ Function to generate unique UFID
def generate_unique_ufid():
    while True:
        ufid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not UserProfile.objects.filter(ufid=ufid).exists():
            return ufid


class Command(BaseCommand):
    help = 'Import users and their financial data from JSON'

    def handle(self, *args, **kwargs):
        with open('accounts/management/commands/dummy.json', 'r') as file:
            data = json.load(file)

        try:
            with transaction.atomic():
                for user_data in data['users']:
                    
                    # ✅ Access dictionary keys properly
                    user_id = user_data.get('user_id')
                    if not user_id:
                        self.stdout.write(self.style.ERROR('Missing user_id. Skipping...'))
                        continue

                    username = f"{user_id.lower()}@example.com"
                    password = '123'  # Default password
                    email = f"{user_id.lower()}@example.com"

                    # ✅ Create User
                    user, created = User.objects.get_or_create(username=username, email=email)
                    if created:
                        user.set_password(password)
                        user.save()

                    # ✅ Generate unique PAN and UFID
                    pan = generate_random_pan()
                    ufid = generate_unique_ufid()

                    # ✅ Create UserProfile
                    profile, _ = UserProfile.objects.get_or_create(
                        user=user,
                        ufid=ufid,  
                        pan=pan,  
                        address=user_data.get('location', ''),
                        phone_number=user_data.get('phone', '')
                    )

                    # ✅ Create Bank Accounts
                    bank_accounts = user_data.get('bank_accounts', {})
                    
                    for acc_type, acc_data in bank_accounts.items():
                        if isinstance(acc_data, list):  # Handle multiple accounts
                            for acc in acc_data:
                                BankAccount.objects.create(
                                    user_profile=profile,
                                    account_type=acc_type.replace('_', ' ').title(),
                                    balance=acc.get('balance', 0),
                                    interest_rate=acc.get('interest_rate', None),
                                    bank_name=acc.get('bank', 'Unknown')
                                )
                        else:
                            BankAccount.objects.create(
                                user_profile=profile,
                                account_type=acc_type.replace('_', ' ').title(),
                                balance=acc_data.get('balance', 0),
                                interest_rate=acc_data.get('interest_rate', None),
                                bank_name=acc_data.get('bank', 'Unknown')
                            )

                    # ✅ Create Demat Account
                    demat_data = user_data.get('demat_account', {})
                    demat_acc, _ = DematAccount.objects.get_or_create(user_profile=profile)

                    for acc_type, acc_data in demat_data.items():
                        if isinstance(acc_data, list):
                            for acc in acc_data:
                                if 'company' in acc:
                                    Stock.objects.create(
                                        demat_account=demat_acc,
                                        company=acc['company'],
                                        shares=acc['shares'],
                                        value=acc['value']
                                    )
                                elif 'fund_name' in acc:
                                    MutualFund.objects.create(
                                        demat_account=demat_acc,
                                        fund_name=acc['fund_name'],
                                        units=acc['units'],
                                        value=acc['value']
                                    )
                        else:
                            MutualFund.objects.create(
                                demat_account=demat_acc,
                                fund_name=acc_type.replace('_', ' ').title(),
                                units=acc_data.get('units', 0),
                                value=acc_data.get('value', 0)
                            )

                    # ✅ Create Credit and Debit Cards
                    cards = user_data.get('credit_debit_cards', {})
                    
                    for card_type, card_list in cards.items():
                        if isinstance(card_list, list):
                            for card in card_list:
                                if 'limit' in card:
                                    CreditCard.objects.create(
                                        user_profile=profile,
                                        bank=card['bank'],
                                        limit=card['limit'],
                                        outstanding=card.get('outstanding', 0)
                                    )
                                elif 'linked_account' in card:
                                    DebitCard.objects.create(
                                        user_profile=profile,
                                        bank=card['bank'],
                                        linked_account=card['linked_account']
                                    )

                    # ✅ Create Assets
                    assets = user_data.get('assets', {})
                    for asset_type, asset_data in assets.items():
                        if isinstance(asset_data, list):
                            for asset in asset_data:
                                Asset.objects.create(
                                    user_profile=profile,
                                    asset_type=asset_type.replace('_', ' ').title(),
                                    value=asset['value']
                                )
                        else:
                            Asset.objects.create(
                                user_profile=profile,
                                asset_type=asset_type.replace('_', ' ').title(),
                                value=asset_data.get('value', 0)
                            )

                    # ✅ Create Debts and Liabilities
                    debts = user_data.get('debt_liabilities', {})
                    for debt_type, debt_list in debts.items():
                        if isinstance(debt_list, list):
                            for debt in debt_list:
                                Debt.objects.create(
                                    user_profile=profile,
                                    debt_type=debt_type.replace('_', ' ').title(),
                                    amount=debt['amount'],
                                    interest_rate=debt['interest_rate'],
                                    tenure_years=debt['tenure_years'],
                                    bank=debt['bank']
                                )

                    # ✅ Create Insurance
                    insurance = user_data.get('insurance', {})
                    for ins_type, ins_data in insurance.items():
                        Insurance.objects.create(
                            user_profile=profile,
                            insurance_type=ins_type.replace('_', ' ').title(),
                            coverage=ins_data.get('coverage', None),
                            sum_assured=ins_data.get('sum_assured', None),
                            premium=ins_data.get('premium', None)
                        )

                    # ✅ Create Retirement Accounts
                    retirement = user_data.get('retirement_accounts', {})
                    for acc_type, acc_data in retirement.items():
                        RetirementAccount.objects.create(
                            user_profile=profile,
                            account_type=acc_type.replace('_', ' ').title(),
                            balance=acc_data.get('balance', 0),
                            annual_contribution=acc_data.get('annual_contribution', None)
                        )

                self.stdout.write(self.style.SUCCESS('Data imported successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
