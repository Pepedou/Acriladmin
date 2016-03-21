from django import forms
from django.conf import settings
from django.forms import ModelForm
from finances.models import Order


class AddOrChangeOrderForm(ModelForm):
    """
    Custom form for adding or changing an order.
    """
    discount_percentage = forms.IntegerField(label='Porcentaje de descuento', initial=0)

    class Meta:
        model = Order
        fields = '__all__'

    class Media:
        js = (
            settings.JQUERY_LIB,
            'finances/scripts/addOrChangeOrderForm.js',
        )
