from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.OrderService)
admin.site.register(models.Executor)
admin.site.register(models.Category)

