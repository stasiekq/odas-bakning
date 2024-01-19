from django.urls import path
from .views import HomeView, registration_view, login_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
]