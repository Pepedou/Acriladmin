from finances.models import ProductPrice, MaterialCost
from rest_framework import serializers


class ProductPriceSerializer(serializers.ModelSerializer):
    """
    Class that serializes a product price.
    """

    class Meta:
        model = ProductPrice
        fields = ('product', 'price', 'authorized_by',)


class MaterialCostSerializer(serializers.ModelSerializer):
    """
    Class that serializes a material cost.
    """

    class Meta:
        model = MaterialCost
        fields = ('material', 'cost', 'authorized_by',)
