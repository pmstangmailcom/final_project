
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from . import models, forms
from .models import OrderService, Executor


# Create your views here.


@login_required(login_url='user_login')
def order_details(request, id: int):
    order = get_object_or_404(OrderService.objects, id=id)

    return render(request, 'services/order_details.html', {'order': order, })

@login_required(login_url='user_login')
def add_new_order(request):
    if request.method == 'POST':
        form = forms.ServicesForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user_id = request.user

            new_order.save()
            return redirect('services:order_details', new_order.id)
        else:
            return render(request, 'services/add_new_order.html', {'form': form})
    else:
        form = forms.ServicesForm()
        return render(request, 'services/add_new_order.html', {'form': form})

@login_required(login_url='user_login')
def update_order(request, id):
    order = get_object_or_404(OrderService.objects, id=id)
    if request.user != order.user_id:
        return redirect('user_login')
    form = forms.ServicesForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('services:order_details', order.id)
    return render(request, 'services/update.html', {'form': form, 'order': order})

@login_required(login_url='user_login')
def delete_order(request, id):
    order = get_object_or_404(OrderService.objects, id=id)
    if request.user != order.user_id:
        # messages.info(request, 'You can not delete order you did not create')
        return redirect('user_login')
    order.delete()
    orders = models.OrderService.objects.all()
    return render(request, 'services/user_orders.html', {'orders': orders, })

def all_orders(request):
    orders = models.OrderService.objects.all()
    return render(request, 'services/index.html', {'orders': orders, })

@login_required(login_url='user_login')
def user_orders(request):
    orders = models.OrderService.objects.filter(user_id=request.user)

    return render(request, 'services/user_orders.html', {'orders': orders, })


@login_required(login_url='user_login')
def accept_order(request, id: int):
    order = get_object_or_404(OrderService.objects, id=id)
    order.is_accepted = True
    order.executor = request.user.executor
    order.executor.order_accepted_num += 1
    order.save()
    order.executor.save()
    return redirect('services:order_details', order.id)

@login_required(login_url='user_login')
def done_order(request, id: int):
    order = get_object_or_404(OrderService.objects, id=id)
    order.is_done = True
    order.executor = request.user.executor
    order.executor.order_done_num += 1
    order.save()
    order.executor.save()
    return redirect('services:order_details', order.id)


def new_executor(request):
    if request.method == 'POST':
        form = forms.ExecutorForm(request.POST)
        if form.is_valid():
            new_executor = form.save(commit=False)
            new_executor.user_id = request.user
            new_executor.save()
            return redirect('services:new_executor', new_executor.id)
        else:
            return render(request, 'services/profile.html', {'form': form})
    else:
        form = forms.ExecutorForm()
        return render(request, 'services/profile.html', {'form': form})

@login_required(login_url='user_login')
def executor_details(request, id: int):
    executor = get_object_or_404(Executor.objects, id=id)

    return render(request, 'services/profile.html', {'executor': executor, })

def check_group(request):
    return request.user.groups.filter(name='Staff').exist()



