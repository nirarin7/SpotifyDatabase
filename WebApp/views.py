from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    context = {}
    return render(request, 'home/index.html', context)

def login(request):
    context = {}
    return render(request, 'login/login.html', context)

def sign_in(request):
    return redirect(index)

def sing_out(request):
    return redirect(login)

def create_account_page(request):
    context = {}
    return render(request, 'login/create_account.html', context)

def create_account(request):
    return redirect(login)