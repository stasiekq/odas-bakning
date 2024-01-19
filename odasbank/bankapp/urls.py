from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('make_transfer/', make_transfer_view, name='make_transfer'),
    path('make_transfer_confirmation/', make_transfer_confirmation_view, name='make_transfer_confirmation'),
    path('logout', logout_view, name='logout'),
    path('transfer_history/', transfer_history_view, name='transfer_history'),
    path('sensitive_data/', sensitive_data_view, name='sensitive_data')
]