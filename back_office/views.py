from back_office.models import Address, Client
from dal import autocomplete
from django.db.models import Q


class AddressAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the Address entity.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            query_set = Address.objects.none()

        elif self.q:
            query_set = Address.objects.filter(Q(street__icontains=self.q) |
                                               Q(city__name__istartswith=self.q) |
                                               Q(state__name__istartswith=self.q) |
                                               Q(country__name__istartswith=self.q))
        else:
            query_set = Address.objects.all()

        return query_set


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the Client entity.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            query_set = Client.objects.none()

        elif self.q:
            query_set = Client.objects.filter(name__icontains=self.q)
        else:
            query_set = Client.objects.all()

        return query_set
