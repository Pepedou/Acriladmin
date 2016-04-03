from django.conf import settings
from django.forms import ModelForm
from inventories.models import ProductDefinition


class AddOrChangeProductDefinitionForm(ModelForm):
    """
    Custom form for adding or changing a product definition.
    """

    class Meta:
        model = ProductDefinition
        fields = '__all__'

    class Media:
        js = (
            settings.JQUERY_LIB,
            'inventories/scripts/addOrChangeProductDefinitionForm.js',
        )
