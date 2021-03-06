from django import forms
from . import models


class ServicesForm(forms.ModelForm):
    class Meta:
        model = models.OrderService
        fields = ('name', 'category', 'notes', 'condition')


class ExecutorForm(forms.ModelForm):
    class Meta:
        model = models.Executor
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'order_accepted_num': forms.HiddenInput(),
            'order_done_num': forms.HiddenInput(),
        }
