from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from accounts.models import Stock, DematAccount, UserProfile  # Your models
from django.contrib.auth.models import User


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
