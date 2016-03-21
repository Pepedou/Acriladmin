from django.forms import ModelForm
from finances.models import ProductPrice
from inventories.models import ProductDefinition


class AddOrChangeProductPriceForm(ModelForm):
    """
    Custom form for adding or changing a product price.
    """

    class Meta:
        model = ProductPrice
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AddOrChangeProductPriceForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = ProductDefinition.get_products_without_price()
