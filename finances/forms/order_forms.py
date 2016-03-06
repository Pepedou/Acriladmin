from django import forms
from django.conf import settings
from django.forms import ModelForm
from finances.models import Order

if settings.DEBUG:
    jquery_lib = 'http://code.jquery.com/jquery-1.12.1.js'
else:
    jquery_lib = 'http://code.jquery.com/jquery-1.12.1.min.js'


class AddOrChangeOrderForm(ModelForm):
    """
    Custom form for adding or changing an order.
    """
    discount_percentage = forms.IntegerField(label='Porcentaje de descuento')

    class Meta:
        model = Order
        fields = '__all__'

    class Media:
        js = (
            jquery_lib,
            'finances/scripts/addOrChangeOrderForm.js',
        )
