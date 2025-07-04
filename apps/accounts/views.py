from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, loginUserForm

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == "POST":
        form = loginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Невірне ім\'я користувача або пароль.')
    else:
        form = loginUserForm()
    return render(request, "login.html", {'form': form})

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = CreateUserForm()
    return render(request, "accounts/register.html", {'form': form})

@login_required
def profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)