from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from accounts.models import Stock, DematAccount, UserProfile  # Your models
from django.contrib.auth.models import User
from django.http import JsonResponse
import random


class PortfolioAPIView(APIView):
    """
    API View to handle user's portfolio:
    - GET: Retrieve total portfolio value, stocks, and default risk score
    - POST: Submit updated stock portfolio and risk profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET request:
        - Fetch user's stocks
        - Calculate total portfolio value
        - Return risk score (default 5)
        """
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)

            # Fetch all stocks related to the user's demat accounts
            demat_accounts = user_profile.demat_accounts.all()

            stocks = Stock.objects.filter(demat_account__in=demat_accounts)

            # Calculate total portfolio value
            total_value = stocks.aggregate(total=Sum('value'))['total'] or 0

            # Serialize stocks data
            stocks_data = [
                {
                    "company": stock.company,
                    "shares": stock.shares,
                    "value": stock.value
                }
                for stock in stocks
            ]

            response_data = {
                "total_value": total_value,
                "risk_score": 5,  # Default risk score
                "stocks": stocks_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        Handle POST request:
        - Update user's portfolio
        - Save investment horizon and monthly investment
        """
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)

            # Extract portfolio data from request
            portfolio_data = request.data.get('portfolio', {})
            risk_profile_data = request.data.get('risk_profile', {})

            # Update portfolio stocks
            stocks = portfolio_data.get('stocks', [])

            for stock_data in stocks:
                company = stock_data.get('company')
                shares = stock_data.get('shares', 0)
                value = stock_data.get('value', 0)

                # Check if the stock exists or create a new one
                demat_account = user_profile.demat_accounts.first()

                stock, created = Stock.objects.get_or_create(
                    demat_account=demat_account,
                    company=company,
                    defaults={'shares': shares, 'value': value}
                )

                if not created:
                    stock.shares = shares
                    stock.value = value
                    stock.save()

            # Save risk profile data
            investment_horizon = risk_profile_data.get('investment_horizon', 0)
            monthly_investment = risk_profile_data.get('monthly_investment', 0)

            # Example: Save this data to the UserProfile or a separate model
            user_profile.investment_horizon = investment_horizon
            user_profile.monthly_investment = monthly_investment
            user_profile.save()

            return Response(
                {"message": "Portfolio updated successfully"},
                status=status.HTTP_200_OK
            )

        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


obj1 = {
    "users": [
        {
            "user_id": "R001",
            "name": "Sharma Retail Pvt Ltd",
            "business_type": "Retail",
            "location": "Delhi",
            "annual_revenue": 25000000,
            "business_income": 8000000,
            "sales": {
                "monthly_sales": 2000000,
                "online_sales": 500000,
                "offline_sales": 1500000
            },
            "inventory": {
                "total_value": 5000000,
                "categories": [
                    {
                        "category": "Electronics",
                        "value": 2000000
                    },
                    {
                        "category": "Groceries",
                        "value": 1500000
                    },
                    {
                        "category": "Clothing",
                        "value": 1500000
                    }
                ]
            },
            "expenses": {
                "rent": 600000,
                "salaries": 3000000,
                "utilities": 200000,
                "marketing": 500000,
                "insurance": 300000,
                "logistics": 800000
            },
            "investments": {
                "expansion_fund": 1500000,
                "equipment_upgrades": 500000
            },
            "bank_accounts": {
                "business_account": {
                    "balance": 1000000,
                    "bank": "SBI"
                },
                "current_account": {
                    "balance": 500000,
                    "bank": "ICICI Bank"
                },
                "fixed_deposits": [
                    {
                        "amount": 2000000,
                        "interest_rate": 6.5,
                        "tenure_years": 3,
                        "bank": "HDFC Bank"
                    }
                ],
                "recurring_deposits": {
                    "monthly_deposit": 20000,
                    "interest_rate": 6.0,
                    "tenure_years": 5,
                    "bank": "Axis Bank"
                }
            },
            "loans": {
                "business_loan": {
                    "amount": 5000000,
                    "interest_rate": 9.0,
                    "tenure_years": 7,
                    "bank": "PNB"
                },
                "working_capital_loan": {
                    "amount": 2000000,
                    "interest_rate": 10.5,
                    "bank": "Kotak Mahindra Bank"
                }
            },
            "assets": {
                "real_estate": [
                    {
                        "type": "Retail Store",
                        "location": "Delhi",
                        "value": 10000000
                    }
                ],
                "vehicles": [
                    {
                        "model": "Tata Ace",
                        "value": 800000
                    }
                ],
                "office_equipment": {
                    "total_value": 500000
                }
            },
            "debt_liabilities": {
                "loan_outstanding": 6500000,
                "credit_card_debt": 100000
            },
            "insurance": {
                "business_insurance": {
                    "coverage": 2000000,
                    "premium": 50000
                },
                "employee_health_insurance": {
                    "coverage": 1000000,
                    "premium": 200000
                }
            },
            "business_expansion_plans": {
                "new_stores": [
                    {
                        "location": "Mumbai",
                        "budget": 5000000
                    },
                    {
                        "location": "Bangalore",
                        "budget": 4500000
                    }
                ],
                "ecommerce_investment": 2000000
            },
            "retirement_accounts": {
                "epf": {
                    "balance": 800000,
                    "contribution": 50000
                },
                "nps": {
                    "balance": 500000,
                    "annual_contribution": 100000
                }
            },
            "miscellaneous": {
                "franchise_income": {
                    "monthly_income": 75000,
                    "branches": [
                        "Kolkata",
                        "Chennai"
                    ]
                }
            }
        }
    ]
}

obj2 = {
    "users": [
        {
            "user_id": "R002",
            "name": "FreshMart Supermarket",
            "business_type": "Supermarket Chain",
            "location": "Bangalore",
            "annual_revenue": 40000000,
            "business_income": 12000000,
            "sales": {
                "monthly_sales": 3500000,
                "online_sales": 1000000,
                "offline_sales": 2500000,
                "highest_selling_category": "Groceries",
                "lowest_selling_category": "Home Decor"
            },
            "inventory": {
                "total_value": 8000000,
                "categories": [
                    {
                        "category": "Groceries",
                        "value": 3000000
                    },
                    {
                        "category": "Dairy & Beverages",
                        "value": 1500000
                    },
                    {
                        "category": "Electronics",
                        "value": 1000000
                    },
                    {
                        "category": "Personal Care",
                        "value": 1500000
                    }
                ]
            },
            "expenses": {
                "rent": 1200000,
                "salaries": 5000000,
                "utilities": 500000,
                "marketing": 700000,
                "insurance": 400000,
                "logistics": 1500000
            },
            "investments": {
                "warehouse_expansion": 3000000,
                "franchise_development": 2500000
            },
            "bank_accounts": {
                "business_account": {
                    "balance": 2000000,
                    "bank": "HDFC Bank"
                },
                "current_account": {
                    "balance": 750000,
                    "bank": "Axis Bank"
                },
                "fixed_deposits": [
                    {
                        "amount": 5000000,
                        "interest_rate": 6.8,
                        "tenure_years": 4,
                        "bank": "SBI"
                    }
                ],
                "recurring_deposits": {
                    "monthly_deposit": 25000,
                    "interest_rate": 6.2,
                    "tenure_years": 3,
                    "bank": "ICICI Bank"
                }
            },
            "loans": {
                "business_loan": {
                    "amount": 7000000,
                    "interest_rate": 8.7,
                    "tenure_years": 10,
                    "bank": "HDFC Bank"
                },
                "inventory_loan": {
                    "amount": 3000000,
                    "interest_rate": 9.5,
                    "bank": "Kotak Mahindra Bank"
                }
            },
            "assets": {
                "real_estate": [
                    {
                        "type": "Supermarket Premises",
                        "location": "Bangalore",
                        "value": 15000000
                    }
                ],
                "vehicles": [
                    {
                        "model": "Tata 407",
                        "value": 1200000
                    },
                    {
                        "model": "Mahindra Bolero Pickup",
                        "value": 900000
                    }
                ],
                "office_equipment": {
                    "total_value": 800000
                }
            },
            "debt_liabilities": {
                "loan_outstanding": 10000000,
                "credit_card_debt": 150000
            },
            "insurance": {
                "business_insurance": {
                    "coverage": 3000000,
                    "premium": 70000
                },
                "employee_health_insurance": {
                    "coverage": 2000000,
                    "premium": 350000
                }
            },
            "business_expansion_plans": {
                "new_supermarkets": [
                    {
                        "location": "Hyderabad",
                        "budget": 7000000
                    },
                    {
                        "location": "Pune",
                        "budget": 6500000
                    }
                ],
                "ecommerce_investment": 3000000
            },
            "retirement_accounts": {
                "epf": {
                    "balance": 1200000,
                    "contribution": 70000
                },
                "nps": {
                    "balance": 750000,
                    "annual_contribution": 120000
                }
            },
            "miscellaneous": {
                "franchise_income": {
                    "monthly_income": 120000,
                    "branches": [
                        "Mysore",
                        "Coimbatore"
                    ]
                }
            }
        }
    ]
}

# List of objects
data = [obj1, obj2]

def get_random_financial_data(request):
    """API to return random financial data"""
    random_data = random.choice(data)
    return JsonResponse(random_data, safe=False)