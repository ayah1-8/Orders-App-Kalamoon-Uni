from django.forms import ModelForm
from django.forms import Form, ModelForm, DateField, widgets
from django import forms

from .models import *

class AnnualNeedsForm(ModelForm):
    class Meta:
        model = AnnualNeed
        fields = ['YearDate','RequestingParty','user']
        widgets = {
            'YearDate': widgets.DateInput(attrs={'type': 'date'})
        }


class OrderForm(ModelForm):
    
    class Meta:
        model = Order
        fields = '__all__'
        #fields = ['FirstSemsQuantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].widget.attrs.update({'class': 'drop'})
        self.fields['FirstSemsQuantity'].widget.attrs.update({'class': 'number'})
        self.fields['SecondSemsQuantity'].widget.attrs.update({'class': 'number'})
        self.fields['ThirdSemsQuantity'].widget.attrs.update({'class': 'number'})
        self.fields['Total'].widget.attrs.update({'class': 'number'})
        self.fields['Description'].widget.attrs.update({'rows': '2','class': 'text','placeholder':'Description'})
        self.fields['FirstBrand'].widget.attrs.update({'class': 'text','placeholder':'FirstBrand'})
        self.fields['SecondBrand'].widget.attrs.update({'class': 'text','placeholder':'SecondBrand'})
        self.fields['ThirdBrand'].widget.attrs.update({'class': 'text','placeholder':'ThirdBrand'})
        self.fields['FlowRate'].widget.attrs.update({'class': 'number'})
        self.fields['Unit'].widget.attrs.update({'class': 'number'})
        self.fields['ApproxPrice'].widget.attrs.update({'class': 'number'})
        self.fields['annualneed'].widget.attrs.update({'class': 'drop'})


    def clean_comment(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                return instance.comment
            else:
                return self.cleaned_data['comment']
    