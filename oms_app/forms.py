from main.models import *
from django.forms import ModelForm
from django.forms import Form, ModelForm, DateField, widgets
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'comment'})
