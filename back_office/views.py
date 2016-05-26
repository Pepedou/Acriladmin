from back_office.models import Address
from dal import autocomplete
from django.db.models import Q


class AddressAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the Address entity.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Address.objects.none()

        query_set = Address.objects.all()

        if self.q:
            query_set = query_set.filter(Q(street__icontains=self.q) |
                                         Q(city__name__istartswith=self.q) |
                                         Q(state__name__istartswith=self.q) |
                                         Q(country__name__istartswith=self.q))

        return query_set
