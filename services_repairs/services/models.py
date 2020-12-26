from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Executor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    mail = models.CharField(max_length=20)
    category = models.ForeignKey(Category, related_name='executor_to_category', verbose_name='category',
                                 on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.name}({self.category})'


class OrderService(models.Model):
    name = models.TextField(max_length=70, verbose_name='name', blank=False)
    category = models.ForeignKey(Category, related_name='order_to_category', verbose_name='category', on_delete=models.RESTRICT)
    notes = models.TextField(max_length=300, verbose_name='notes', blank=False)
    create_on_date = models.DateTimeField(verbose_name='date_entry', auto_now_add=True)
    is_accepted = models.BooleanField()
    is_done = models.BooleanField()
    user_id = models.ForeignKey(User, verbose_name='user', related_name='order_to_user', null=True,
                                            on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}({self.category})'







