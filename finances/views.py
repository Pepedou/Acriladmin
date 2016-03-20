from finances.models import ProductPrice, MaterialCost
from finances.serializers import ProductPriceSerializer, MaterialCostSerializer

from rest_framework import viewsets


class ProductPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product price to be viewed or edited through a RESTful API.
    """
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer


class MaterialCostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows material cost to be viewed or edited through a RESTful API.
    """
    queryset = MaterialCost.objects.all()
    serializer_class = MaterialCostSerializer
