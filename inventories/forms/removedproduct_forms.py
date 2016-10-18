from dal import autocomplete
from django.forms import BaseInlineFormSet
from django.forms import ModelForm

from inventories.models import RemovedProduct


class RemovedProductFormset(BaseInlineFormSet):
    """
    Formset used in the ProductRemoval many to one relationship. It's used to pass
    the request to each RemovedProductForm.
    """

    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        self.request = kwargs.pop('request')
        super(RemovedProductFormset, self).__init__(data, files, instance, save_as_new, prefix, queryset, **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super(RemovedProductFormset, self).get_form_kwargs(index)
        form_kwargs['request'] = self.request
        return form_kwargs


class RemovedProductForm(ModelForm):
    """
    Custom form for adding or changing a removed product.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RemovedProductForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RemovedProduct
        fields = "__all__"

        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 })
        }

    def clean(self):
        request = self.request
        cleaned_data = super(RemovedProductForm, self).clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        inventory = request.user.branch_office.productsinventory

        product_inventory_item = inventory.productinventoryitem_set.filter(product=product).first()

        if product_inventory_item is None:
            self.add_error('product', "{0} no cuenta con el producto {1}. Hay que agregarlo al inventario.".format(
                str(inventory), str(product)
            ))
        elif product_inventory_item.quantity < quantity:
            self.add_error('quantity', "{0} sólo cuenta con {} unidades de este producto.".format(
                str(inventory), str(quantity)
            ))

        return cleaned_data
