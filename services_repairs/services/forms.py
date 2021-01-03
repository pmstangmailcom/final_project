from django import forms
from . import models



class ServicesForm(forms.ModelForm):
    class Meta:
        model = models.OrderService
        fields = ('name', 'category', 'notes')
        # fields = '__all__'
        # exclude = ['user_id']

class ExecutorForm(forms.ModelForm):
    class Meta:
        model = models.Executor
        # fields = '__all__'
        fields = ('category',)


