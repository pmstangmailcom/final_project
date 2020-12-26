from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models, forms

# Create your views here.
# def HelloWorldView(request):
#     return HttpResponse('Hello World!!!')

def all_orders(request):
    orders = models.OrderService.objects.all()
    return render(request, 'index.html', {'orders': orders, })


# def add_order(request):
#     order = models.OrderService.objects.all()
#     return render(request, 'services/index.html', {'order': order, })



# Create your views here.
