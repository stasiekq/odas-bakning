from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm, LoginForm


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
            return redirect('home')
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
            return redirect('home')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

class HomeView(TemplateView):
    template_name = 'home.html'