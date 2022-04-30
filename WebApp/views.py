from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect(log_in)

    context = {
        'username': request.user.username
    }
    return render(request, 'home/index.html', context)


def log_in(request):
    context = {}
    return render(request, 'login/login.html', context)


def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home/index.html', {'username': username})
        else:
            messages.error(request, "Invalid Credentials")
            return redirect(log_in)


def sign_out(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect(log_in)


def create_account_page(request):
    return render(request, 'login/create_account.html')


def create_account(request):
    if request.method == "POST":
        username = request.POST["username"]
        emailAddress = request.POST["emailAddress"]
        password = request.POST["password"]

        if User.objects.get(username=username) is not None:
            messages.error(request, "Username is already taken.")
            return render(request, 'login/create_account.html')

        user = User.objects.create_user(username, emailAddress, password)
        user.save()
        messages.success(request, "Your account has successfully been created.")
        return redirect(log_in)

    return render(request, 'login/create_account.html')
