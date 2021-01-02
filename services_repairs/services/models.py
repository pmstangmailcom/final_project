from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='category')

    def __str__(self):
        return self.name


class Executor(models.Model):
    # name = models.CharField(max_length=50, verbose_name='name')
    # last_name = models.CharField(max_length=50, verbose_name='last_name', blank=True, null=True)
    # phone = models.CharField(max_length=20, verbose_name='phone')
    # email = models.EmailField(max_length=20, verbose_name='email', blank=True)
    category = models.ForeignKey(Category, related_name='executor_to_category', verbose_name='category',
                                 on_delete=models.RESTRICT)
    order_accepted_num = models.IntegerField(verbose_name='Order accepted Number', default=0)
    order_done_num = models.IntegerField(verbose_name='Order Done Number', default=0)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, blank=True, null=True, related_name='executor')
    # class Meta:
    #     proxy = True

    def __str__(self):
        return f'{self.user}'
        # return f'{self.user}  ({self.category})'


class OrderService(models.Model):
    name = models.CharField(max_length=250, verbose_name='name', blank=False)
    category = models.ForeignKey(Category, related_name='order_to_category', verbose_name='category',
                                 on_delete=models.RESTRICT)
    notes = models.TextField(max_length=300, verbose_name='notes', blank=False)
    create_on_date = models.DateTimeField(verbose_name='date_order', auto_now_add=True)
    accept_on_date = models.DateTimeField(verbose_name='date_accept_order', auto_now=True)
    done_on_date = models.DateTimeField(verbose_name='date_done_order', auto_now=True)
    is_accepted = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, verbose_name='owner', related_name='order_to_user', null=True,
                                on_delete=models.SET_NULL)
    executor = models.ForeignKey(Executor, related_name='order_to_executor', verbose_name='executor', null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}({self.category})'
