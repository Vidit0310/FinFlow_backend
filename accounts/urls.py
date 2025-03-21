from django.urls import path
from .views import signup, create_userprofile

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('userprofile/', create_userprofile, name='userprofile'),
]
