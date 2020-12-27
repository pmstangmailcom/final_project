from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models, forms

# Create your views here.


def order_details(request, id: int):
    order = models.OrderService.objects.get(id=id)
    if not order:
        raise Exception('No such order')
    return render(request, 'services/index.html', {'order': order, })

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

def update_order(request, id):
    order = models.OrderService.objects.get(id=id)
    form = forms.ServicesForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('services:order_details', order.id)
    return render(request, 'services/update.html', {'form': form, 'order': order})

def delete_order(request, id):

    order = models.OrderService.objects.get(id=id)
    order.delete()
    orders = models.OrderService.objects.all()
    return render(request, 'services/user_orders.html', {'orders': orders, })

def all_orders(request):
    orders = models.OrderService.objects.all()
    return render(request, 'services/index.html', {'orders': orders, })

def user_orders(request):
    orders = models.OrderService.objects.filter(user_id=request.user)
    return render(request, 'services/user_orders.html', {'orders': orders, })

def new_executor(request):
    if request.method == 'POST':
        form = forms.ExecutorForm(request.POST)
        if form.is_valid():
            new_executor = form.save(commit=False)
            new_executor.user_id = request.user
            new_executor.save()
            return redirect('services:order_details', new_executor.id)
        else:
            return render(request, 'services/add_new_order.html', {'form': form})
    else:
        form = forms.ExecutorForm()
        return render(request, 'services/add_new_order.html', {'form': form})


