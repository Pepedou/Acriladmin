from finances.models import ProductPrice
from rest_framework import serializers


class ProductPriceSerializer(serializers.ModelSerializer):
    """
    Class that serializes a product price.
    """

    class Meta:
        model = ProductPrice
        fields = ('product', 'price', 'authorized_by',)

