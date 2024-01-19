from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import FormView, TemplateView
from django.utils.crypto import get_random_string
from django.contrib import messages
import string
from .forms import *


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Nie zapisuj jeszcze użytkownika
            user.balance = 1000
            user.account_number = get_random_string(length=6, allowed_chars=string.digits)
            
            try:
                user.save()  # Zapisz użytkownika
            except Exception as e:
                # Obsłuż błąd zapisu użytkownika (np. wyjątek walidacji)
                # Możesz tutaj wyświetlić komunikat błędu lub logować go
                print(f"Błąd zapisu użytkownika: {e}")
                return render(request, 'register.html', {'form': form})
            
            # Pomyślnie zapisany użytkownik, kontynuuj zalogowanie
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Zalogowano pomyślnie')
            return redirect('dashboard')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})

def make_transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            reciever_account_number = form.cleaned_data['reciever_account_number']
            amount = form.cleaned_data['amount']
            title = form.cleaned_data['title']
            
            sender = request.user
            
            if not User.objects.filter(account_number=reciever_account_number).exists():
                messages.error(request, 'Nie ma takiego użytkownika')
                return redirect('make_transfer')
            
            transfer = Transfer.objects.crerate(
                sender = sender,
                reciever = User.objects.get(account_number=reciever_account_number),
                reciever_name = User.objects.get(account_number=reciever_account_number).username,
                amount = amount,
                title = title
            )
            
            messages.success(request, 'Transfer completed successfully')
            return redirect('make_transfer_confirmation')
    else:
        form = TransferForm()
        
    return render(request, 'make_transfer.html', {'form': form})
            
def make_transfer_confirmation_view(request):
    return render(request, 'make_transfer_confirmation.html')

def logout_view(request):
    logout(request)
    return redirect('home')

class HomeView(TemplateView):
    template_name = 'home.html'
    