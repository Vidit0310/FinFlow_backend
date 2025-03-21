from django.urls import path
from .views import signup, create_userprofile, login_view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('userprofile/', create_userprofile, name='userprofile'),
    path('login/', login_view, name='login'),

]
