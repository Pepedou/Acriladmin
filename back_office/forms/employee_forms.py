from back_office.models import Employee
from dal import autocomplete
from django.forms import ModelForm


class AddOrChangeEmployeeForm(ModelForm):
    """
    Custom form for adding or changing a product price.
    """

    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            'address': autocomplete.ModelSelect2(url='address-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese una calle, ciudad, región o país...',
                                                     'data-minimum-input-length': 3,
                                                 })
        }
