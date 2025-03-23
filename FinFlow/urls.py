from django.contrib import admin
from django.urls import path, include
from .views import PortfolioAPIView, get_random_financial_data

urlpatterns = [
    path('admin/', admin.site.urls),                  
    path('accounts/', include('accounts.urls')),   
    path('api/portfolio/', PortfolioAPIView.as_view(), name='portfolio-api'),
    path('api/financial-data/', get_random_financial_data, name='financial-data')
   
]
