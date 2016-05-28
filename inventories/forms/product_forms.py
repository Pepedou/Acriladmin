from django.forms import ModelForm
from inventories.models import Product


class AddOrChangeProductForm(ModelForm):
    """
    Custom form for adding or changing a product definition.
    """

    class Meta:
        model = Product
        fields = '__all__'

    class Media:
        js = (
            'inventories/scripts/addOrChangeProductForm.js',
        )
