from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, loginUserForm, ChangeAccountDetailsForm
@login_required
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
                return redirect('accounts:profile')
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
    return render(request, "register.html", {'form': form})

@login_required
def profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)


@login_required
def change_account_details(request):
    if request.method == 'POST':
        form = ChangeAccountDetailsForm(request.POST, instance=request.user, user=request.user)

        if form.is_valid():
            user = form.save(commit=False)

            new_password1 = form.cleaned_data.get('new_password1')
            if new_password1:
                user.set_password(new_password1)

            user.save()
            if new_password1:
                update_session_auth_hash(request, user)

            return redirect('accounts:profile')
    else:
        form = ChangeAccountDetailsForm(instance=request.user, user=request.user)
    return render(request, 'change_account_details.html', {'form': form})