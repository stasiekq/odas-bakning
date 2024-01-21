from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', registration_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('make_transfer/', make_transfer_view, name='make_transfer'),
    path('make_transfer_confirmation/', make_transfer_confirmation_view, name='make_transfer_confirmation'),
    path('logout', logout_view, name='logout'),
    path('transfer_history/', transfer_history_view, name='transfer_history'),
    path('sensitive_data/', sensitive_data_view, name='sensitive_data'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', TemplateView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('automatic_logout_info/', AutomaticLogoutInfoView.as_view(), name='automatic_logout_info'),
]