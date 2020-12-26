from django import forms
from . import models



class ServicesForm(forms.Form):
    class Meta:
        models = models.OrderService
        fields = '__all__'

