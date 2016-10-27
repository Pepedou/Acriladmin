from django.forms import ModelForm

from inventories.models import ProductRemoval


class AddOrChangeProductRemovalForm(ModelForm):
    """
    Custom form for adding or changing a product removal.
    """

    class Meta:
        model = ProductRemoval
        fields = "__all__"

    def clean(self):
        cleaned_data = super(AddOrChangeProductRemovalForm, self).clean()
        cause = cleaned_data.get('cause')
        provider = cleaned_data.get('provider')
        product_transfer = cleaned_data.get('product_transfer_reception')

        if cause is not None:
            if cause == ProductRemoval.CAUSE_PROVIDER:
                if not provider:
                    self.add_error('provider', "Se requiere especificar un proveedor.")
            elif cause == ProductRemoval.CAUSE_TRANSFER:
                if not product_transfer:
                    self.add_error('product_transfer_reception',
                                   "Se requiere especificar una transferencia de producto.")

        return cleaned_data
