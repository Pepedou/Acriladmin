from finances.models import ProductPrice
from finances.serializers import ProductPriceSerializer

from rest_framework import viewsets


class ProductPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product price to be viewed or edited.
    """
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
