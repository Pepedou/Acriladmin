from dal import autocomplete
from django.forms import ModelForm
from inventories.models import ExchangedProduct, ReturnedProduct


class AddOrChangeReturnedProductTabularInlineForm(ModelForm):
    """
    Custom form for adding or changing a returned product.
    """

    class Meta:
        model = ReturnedProduct
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese un producto',
                                                     'data-minimum-input-length': 1,
                                                 })
        }


class AddOrChangeExchangedProductTabularInlineForm(ModelForm):
    """
    Custom form for adding or changing an exchanged product.
    """

    class Meta:
        model = ExchangedProduct
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese un producto',
                                                     'data-minimum-input-length': 1,
                                                 })
        }
