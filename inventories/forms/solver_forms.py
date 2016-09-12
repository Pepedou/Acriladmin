from django.forms import CheckboxSelectMultiple, BooleanField
from django.forms import DecimalField, IntegerField, forms
from django.forms import MultipleChoiceField

from inventories.models import Product


class SolverForm(forms.Form):
    """

    """
    length = DecimalField(max_digits=10, decimal_places=2, min_value=0, label='Longitud (m)')
    width = DecimalField(max_digits=10, decimal_places=2, min_value=0, label='Anchura (m)')
    quantity = IntegerField(max_value=10000, min_value=1, label='Cantidad')
    product_lines = MultipleChoiceField(choices=Product.LINE_TYPES, widget=CheckboxSelectMultiple,
                                        label='Líneas de producto')
    select_all_product_lines = BooleanField(required=False, label='Todas')

    class Media:
        js = ['inventories/scripts/solver.js']
