from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required

# Create your views here.

User = get_user_model()

@unauthenticated_user
def register_view(request):
    print('register_view()-----------------')
    # ----------------------------------
    if request.method == "GET":
        print('GET method-----------------')
        return render(request, 'accounts/register.html', context={'form': RegisterForm()})
    # ----------------------------------
    else:
        print('POST method-----------------')
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            print("form is valid---------")
            uid = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            pwd = form.cleaned_data.get('password')
            pwd2 = form.cleaned_data.get('password2')
            try:
                if pwd != pwd2:
                    messages.error(request, "Passwords must be the same")
                    raise ValidationError("passwords, must be the same")

                user = User.objects.create_user(username=uid, email=email, password=pwd)
            except:
                user = None

            if user != None:
                return redirect('login')
            else:
                request.session['register error'] = 1

        return render(request, 'accounts/register.html', context={'form': form})

@unauthenticated_user
def login_view(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html', {'form': LoginForm()})
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            uid_email = form.cleaned_data.get('login')
            pwd = form.cleaned_data.get('password')
            # if user gave email as login
            user_qs = get_user_model().objects.filter(email__iexact=uid_email)
            if user_qs:
                username = user_qs[0].username
                user = authenticate(request, username=username, password=pwd)
            # if user gave username as login
            elif get_user_model().objects.filter(username__iexact=uid_email):
                user = authenticate(request, username=uid_email, password=pwd)
            else:
                user = None
            # if user exists - login & redirect
            if user != None:
                request.session['invalid_user'] = 0
                login(request, user)
                return redirect('/')
            # if user doesn't exists render login page
            else:
                request.session['invalid_user'] = 1

        return render(request, 'accounts/login.html', {'form': LoginForm()})

def logout_view(request):
    logout(request)
    return redirect('/')