from dal import autocomplete
from django.forms import ModelForm
from inventories.models import ProductComponent


class AddOrChangeProductComponentInlineForm(ModelForm):
    """
    Custom form for adding or changing a product component.
    """

    class Meta:
        model = ProductComponent
        fields = '__all__'
        widgets = {
            'material': autocomplete.ModelSelect2(url='material-autocomplete',
                                                  attrs={
                                                      'data-placeholder': 'Ingrese un material',
                                                      'data-minimum-input-length': 1,
                                                  })
        }
