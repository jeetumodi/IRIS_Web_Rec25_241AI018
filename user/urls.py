from django.urls import path
from .views import profile
from authenticate.views import home

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('home/',home,name='home'),
]
