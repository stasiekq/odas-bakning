from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from functools import wraps
import string
from .forms import *
from .models import *

def otp_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/account/login')
        if not request.user.is_verified():
            return redirect('/account/two_factor/setup')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def registration_view(request):
    if request.user.is_authenticated:
            return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.balance = 1000
            user.account_number = get_random_string(length=6, allowed_chars=string.digits)
            
            try:
                user.save()
                user.connect_sensitive_data(form.cleaned_data['credit_card_number'], form.cleaned_data['id_number'])
                
            except Exception as e:
                print(f"Błąd zapisu użytkownika: {e}")
                return render(request, 'register.html', {'form': form})
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/account/two_factor/setup')
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})




@otp_required
def dashboard_view(request):
    user = request.user
    account_balance = user.balance
    account_number = user.account_number
    
    context = {
        'account_balance': account_balance,
        'account_number': account_number
    }
    
    return render(request, 'dashboard.html', context)

@otp_required
def make_transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            reciever_account_number = form.cleaned_data['reciever_account_number']
            reciever_name = form.cleaned_data['reciever_name']
            amount = form.cleaned_data['amount']
            title = form.cleaned_data['title']
            
            sender = request.user
            
            if not User.objects.filter(account_number=reciever_account_number).exists():
                messages.error(request, 'Nie ma takiego użytkownika')
                return redirect('make_transfer')
            
            reciever = User.objects.get(account_number=reciever_account_number)
            
            transfer = Transfer.objects.create(
                sender = sender,
                reciever = User.objects.get(account_number=reciever_account_number),
                reciever_name = reciever_name,
                amount = amount,
                title = title
            )
            
            if transfer.validate():
                transfer.save()
                transfer.execute()
                messages.success(request, 'Transfer completed successfully')
                return redirect('make_transfer_confirmation')
            else:
                messages.error(request, 'Insufficient funds')
                return redirect('make_transfer')
    else:
        form = TransferForm()
        
    return render(request, 'make_transfer.html', {'form': form})
            
@otp_required
def make_transfer_confirmation_view(request):
    return render(request, 'make_transfer_confirmation.html')

@otp_required
def transfer_history_view(request):
    user = request.user
    incoming_transfers = Transfer.objects.filter(reciever=user).order_by('-date')
    outgoing_transfers = Transfer.objects.filter(sender=user).order_by('-date')
    
    return render(request, 'transfer_history.html', {'incoming_transfers': incoming_transfers, 'outgoing_transfers': outgoing_transfers})

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@otp_required
def sensitive_data_view(request):
    user = request.user

    try:
        sensitive_data = SensitiveData.objects.get(user=user)
    except:
        sensitive_data = None

    return render(request, 'sensitive_data.html', {'user': user, 'sensitive_data': sensitive_data})

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('password_change_done')
    
class AutomaticLogoutInfoView(View):
    template_name = 'automatic_logout_info.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)