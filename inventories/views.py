from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from inventories.models import ProductsInventory


class ProductInventoryView(ListView):
    """
    Class view that generates the HTTP responses for all product inventories
    requests.
    """
    template_name = 'inventories/product_inventory.html'
    context_object_name = 'product_inventory_items'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.primary_key = kwargs['pk']
        return super(ProductInventoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        products_inventory = ProductsInventory.objects.filter(pk=self.primary_key).first()

        if products_inventory is not None:
            return products_inventory.items.all()
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(ProductInventoryView, self).get_context_data(**kwargs)
        context['title'] = "Inventario de productos {0}".format(self.primary_key)
        context['site_title'] = AdminSite.site_title
        context['site_header'] = AdminSite.site_header

        return context
