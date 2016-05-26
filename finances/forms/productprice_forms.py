from dal import autocomplete
from django.forms import ModelForm
from finances.models import ProductPrice
from inventories.models import Product


class AddOrChangeProductPriceForm(ModelForm):
    """
    Custom form for adding or changing a product price.
    """

    class Meta:
        model = ProductPrice
        fields = "__all__"
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese un producto',
                                                     'data-minimum-input-length': 1,
                                                 })
        }

    def __init__(self, *args, **kwargs):
        super(AddOrChangeProductPriceForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_products_without_price()
