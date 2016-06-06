import pyexcel
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from inventories.models import ProductsInventory
from inventories.validators import validate_file_extension


class AddOrChangeProductsInventoryForm(ModelForm):
    """
    Custom form for adding or changing a products inventory.
    """
    excel_file = forms.FileField(required=False, max_length=50, allow_empty_file=False,
                                 label='Cargar inventario (.xlsx, .xls)')

    class Meta:
        model = ProductsInventory
        fields = '__all__'

    def clean_excel_file(self):
        """
        Validates that the uploaded file has a valid extension and is formatted
        properly.
        """
        super(AddOrChangeProductsInventoryForm, self).clean_excel_file()
        valid_extensions = ['.xls', '.xlsx']

        file = self.cleaned_data.get('excel_file')

        if file is None:
            return

        validate_file_extension(file, valid_extensions)

        file_extension = file.name.split(".")[1]

        sheet = pyexcel.load_from_memory(file_extension, file.read(), name_columns_by_row=0,
                                         name_rows_by_column=-1)
        excel_data = pyexcel.to_dict(sheet)

        if 'SKU' not in excel_data:
            raise ValidationError(
                'El archivo cargado no cuenta con una columna titulada "SKU". Por favor, agregue la columna.')

        if 'Cantidad' not in excel_data:
            raise ValidationError('El archivo cargado no cuenta con una columna titulada "Cantidad". '
                                  'Por favor, agregue la columna.')

        num_sku_items = len(excel_data['SKU'])
        num_quantity_items = len(excel_data['Cantidad'])

        if num_sku_items != num_quantity_items:
            raise ValidationError('Debe existir una correspondencia 1:1 en los elementos del inventario. '
                                  'Se identificaron {0} productos en la columna de SKU pero {1} en la columna de Cantidad. '
                                  'Verifique que sean iguales.'.format(num_sku_items, num_quantity_items))

        for i, item in enumerate(excel_data['SKU']):
            if item.isspace():
                raise ValidationError('El SKU del producto en la fila {0} está vacío.'.format(i))

        for i, item in enumerate(excel_data['Cantidad']):
            if not item:
                raise ValidationError('Debe existir una correspondencia 1:1 en los elementos del inventario. '
                                      'El producto "{0}" no cuenta con una cantidad especificada en la fila {1}.'
                                      .format(excel_data['SKU'][i], i + 2))

            try:
                int(item)
            except ValueError:
                raise ValidationError(
                    'La columna de "Cantidad" sólo puede contener números enteros. {0} no es un valor válido'.format(
                        item))
