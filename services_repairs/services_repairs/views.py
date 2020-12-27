from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import RegisterForm, LoginForm
from . import forms

def user_register(request):
    if request.user.is_authenticated:
        return redirect('all_orders')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
                new_user = form.cleaned_data.get('username')

                return render(request, 'account/register_done.html', {'new_user': new_user})
        context = {'form': form}
        return render(request, 'account/register.html', context)


def user_login(request):

    if request.user.is_authenticated:
        return redirect('all_orders')
    else:
        if request.method == 'POST':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = authenticate(request, username=cleaned_data['username'], password=cleaned_data['password'])

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('services:user_orders')

                    return HttpResponse('Disabled account')
                else:
                    return HttpResponse('Invalid login')

            context = {}
            return render(request, 'account/login.html', context)
        else:
            form = forms.LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')



