
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
    return render(request, 'services/all_orders.html', {'orders': orders, })

@login_required(login_url='user_login')
def user_orders(request):
    orders = models.OrderService.objects.filter(user_id=request.user)
    executor = models.Executor.objects.filter(user_id=request.user)

    if executor:
        orders_by_executor = models.OrderService.objects.filter(executor__user=request.user)
        orders_category_executor = models.OrderService.objects.filter(category=request.user.executor.category, is_accepted=False)
        context = {
            'orders': orders,
            'orders_by_executor': orders_by_executor,
            'orders_category_executor': orders_category_executor
        }
    else:
        context = {'orders': orders,}

    return render(request, 'services/user_orders.html', context)


@login_required(login_url='user_login')
def accept_order(request, id: int):
    order = get_object_or_404(OrderService.objects, id=id)
    if order.category == request.user.executor.category:
        order.is_accepted = True
        order.executor = request.user.executor
        order.executor.order_accepted_num += 1
        order.save()
        order.executor.save()
        return redirect('services:order_details', order.id)
    else:
        return redirect('services:order_details', order.id)


@login_required(login_url='user_login')
def done_order(request, id: int):
    order = get_object_or_404(OrderService.objects, id=id)
    # if orders_category_executor == request.user:
    if order.user_id == request.user:
        order.is_done = True
        # order.executor = request.user.executor
        order.executor.order_done_num += 1
        order.save()
        order.executor.save()
        return redirect('services:order_details', order.id)
    else:
        return redirect('services:order_details', order.id)

@login_required(login_url='user_login')
def new_executor(request):
    if request.method == 'POST':
        # form = forms.ExecutorForm(request.POST)
        form = forms.ExecutorForm(request.POST or None, instance=request.user)
        if form.is_valid():
            executor = form.save(commit=False)
            # executor.user_id = request.user
            executor.save()
            return redirect('services:executor_profile', executor.id)
        else:
            return render(request, 'services/new_executor.html', {'form': form})
    else:
        form = forms.ExecutorForm()
        return render(request, 'services/new_executor.html', {'form': form})


@login_required(login_url='user_login')
def executor_profile(request, id: int):
    executor = get_object_or_404(Executor.objects, id=id)
    # executor = models.Executor.objects.get(id=id)
    return render(request, 'services/profile.html', {'executor': executor, })

# def check_group(request):
#     return request.user.groups.filter(name='Staff').exist()


# def filter_categories(request):
#     orders_photo = models.OrderService.objects.filter(category__name='Фото, видео', is_done=False)
#     orders_lawyer = models.OrderService.objects.filter(category__name='Юридические услуги', is_done=False)
#     orders_sewing = models.OrderService.objects.filter(category__name='Пошив и ремонт одежды', is_done=False)
#     orders_repair = models.OrderService.objects.filter(category__name='Ремонт бытовой техники', is_done=False)
#     orders_teaching = models.OrderService.objects.filter(category__name='Обучение, репетиторство', is_done=False)
#     context = {
#         'orders_photo': orders_photo,
#         'orders_lawyer': orders_lawyer,
#         'orders_sewing': orders_sewing,
#         'orders_repair': orders_repair,
#         'orders_teaching': orders_teaching,
#     }
#     return render(request, 'categories/photo_video.html',  context)

def filter_photo(request):
    orders_photo = models.OrderService.objects.filter(category__name='Фото, видео', is_done=False)
    executors = models.Executor.objects.filter(category__name='Фото, видео')
    return render(request, 'categories/photo_video.html', {'orders_photo': orders_photo, 'executors': executors})

def filter_lawyer(request):
    orders_lawyer = models.OrderService.objects.filter(category__name='Юридические услуги', is_done=False)
    executors = models.Executor.objects.filter(category__name='Юридические услуги')
    return render(request, 'categories/lawyer.html', {'orders_lawyer': orders_lawyer, 'executors': executors})

def filter_sewing(request):
    orders_sewing = models.OrderService.objects.filter(category__name='Пошив и ремонт одежды', is_done=False)
    executors = models.Executor.objects.filter(category__name='Пошив и ремонт одежды')
    return render(request, 'categories/sewing.html', {'orders_sewing': orders_sewing, 'executors': executors})

def filter_repair(request):
    orders_repair = models.OrderService.objects.filter(category__name='Ремонт бытовой техники', is_done=False)
    executors = models.Executor.objects.filter(category__name='Ремонт бытовой техники')
    return render(request, 'categories/repair.html', {'orders_repair': orders_repair,'executors': executors})

def filter_teaching(request):
    orders_teaching = models.OrderService.objects.filter(category__name='Обучение, репетиторство', is_done=False)
    executors = models.Executor.objects.filter(category__name='Обучение, репетиторство')
    return render(request, 'categories/teaching.html', {'orders_teaching': orders_teaching, 'executors': executors})