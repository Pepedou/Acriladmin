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

    def __init__(self, *args, **kwargs):
        super(AddOrChangeProductPriceForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_products_without_price()
