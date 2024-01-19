from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'