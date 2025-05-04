# account/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Вхід виконано успішно!')
            return redirect('shop:product_list')  # замените на актуальный URL
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'Ви вийшли з акаунту.')
    return redirect('account:login')  # корректно указывать namespace


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна! Вас автоматично увійшло в систему.')
            return redirect('shop:product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})
