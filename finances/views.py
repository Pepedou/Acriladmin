from dal import autocomplete
from django.db.models import Q

from finances.models import ProductPrice, MaterialCost, Invoice
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


class InvoiceAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the Invoice entity.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            query_set = Invoice.objects.none()
        elif self.q:
            query_set = Invoice.objects.filter(Q(folio__icontains=self.q))
        else:
            query_set = Invoice.objects.all()

        return query_set
