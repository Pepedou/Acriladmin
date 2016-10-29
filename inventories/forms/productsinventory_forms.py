import logging

import pyexcel
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm
from django.forms.utils import ErrorList

from inventories.models import ProductsInventory, ProductInventoryItem, Product
from inventories.validators import validate_file_extension

db_logger = logging.getLogger('db')


class AddOrChangeProductsInventoryForm(ModelForm):
    """
    Custom form for adding or changing a products inventory.
    """
    excel_file = forms.FileField(required=False, max_length=50, allow_empty_file=False,
                                 label='Cargar inventario (.xlsx, .xls)')

    class Meta:
        model = ProductsInventory
        fields = '__all__'

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):
        super(AddOrChangeProductsInventoryForm, self).__init__(data, files, auto_id, prefix, initial, error_class,
                                                               label_suffix, empty_permitted, instance)
        self.excel_data_dict = {}

    def clean_excel_file(self):
        """
        Validates that the uploaded file has a valid extension and is formatted
        properly.
        """
        try:
            file = self.cleaned_data.get('excel_file')

            if file is None:
                return

            excel_data = AddOrChangeProductsInventoryForm._excel_file_to_dict(file)

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

            self.excel_data_dict = excel_data
        except Exception as e:
            db_logger.exception(e)
            raise

    @staticmethod
    def _excel_file_to_dict(file):
        """
        Loads an Excel file and transforms it into a dictionary. It uses the first row's cells
        as keys for the dictionary and the columns are the contents.
        :param file: The Excel file to transform.
        :return: A dictionary of arrays.
        """
        valid_extensions = ['.xls', '.xlsx']

        validate_file_extension(file, valid_extensions)

        file_extension = file.name.split(".")[1]
        sheet = pyexcel.load_from_memory(file_extension, file.read(), name_columns_by_row=0, name_rows_by_column=-1)

        return pyexcel.to_dict(sheet)

    def save(self, commit=True):
        """
        Overrides the save method in order to add the product inventory items listed in
        the uploaded Excel file, if one was uploaded.
        """
        try:
            inventory = super(AddOrChangeProductsInventoryForm, self).save(commit)

            if len(self.excel_data_dict) == 0:
                return inventory

            non_existing_products = []

            for i, product_sku in enumerate(self.excel_data_dict['SKU']):
                quantity = self.excel_data_dict['Cantidad'][i]
                new_item = ProductInventoryItem.objects.filter(Q(product__sku=product_sku) &
                                                               Q(inventory=inventory)).first()

                if new_item is None:
                    product = Product.objects.filter(sku=product_sku).first()

                    if product is None:
                        non_existing_products.append(product_sku)
                        continue

                    new_item = ProductInventoryItem()
                    new_item.product = product
                    new_item.inventory = inventory

                new_item.quantity += quantity
                new_item.save()

            return inventory
        except Exception as e:
            db_logger.exception(e)
            raise
