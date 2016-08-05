from rest_framework import serializers

from inventories.models import ProductInventoryItem


class ProductInventoryItemSerializer(serializers.ModelSerializer):
    """
    Class that serializes a product inventory item.
    """

    class Meta:
        model = ProductInventoryItem
        fields = ('product', 'quantity', 'inventory',)
