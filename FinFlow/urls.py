from django.contrib import admin
from django.urls import path, include
from .views import PortfolioAPIView

urlpatterns = [
    path('admin/', admin.site.urls),                  
    path('accounts/', include('accounts.urls')),   
    path('api/portfolio/', PortfolioAPIView.as_view(), name='portfolio-api'),
   
]
