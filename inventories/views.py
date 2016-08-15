import operator
from functools import reduce

from dal import autocomplete
from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from rest_framework import viewsets

from inventories.models import ProductsInventory, MaterialsInventory, ConsumablesInventory, DurableGoodsInventory, \
    Product, Material, Consumable, DurableGood, ProductInventoryItem
from inventories.serializers import ProductInventoryItemSerializer


class ProductInventoryView(ListView):
    """
    Class view that generates the HTTP responses for all product inventories
    requests.
    """
    template_name = 'inventories/inventory.html'
    context_object_name = 'inventory_items'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.primary_key = 0
        self.inventory_name = "Inventario de productos"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.primary_key = kwargs['pk']
        return super(ProductInventoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        products_inventory = ProductsInventory.objects.filter(pk=self.primary_key).first()

        if products_inventory is not None:
            self.inventory_name = products_inventory.name
            inventory_items = products_inventory.productinventoryitem_set.all()
            queryset = []

            for item in inventory_items:
                queryset.append([
                    {
                        "attribute": item.id,
                        "name": "item_id",
                        "type": "hidden"
                    },
                    {
                        "attribute": item.product.id,
                        "name": "product_id",
                        "type": "hidden"
                    },
                    {
                        "attribute": item.product.sku,
                        "name": "product_sku",
                        "type": "label"
                    },
                    {
                        "attribute": item.product.description,
                        "name": "product_description",
                        "type": "label"
                    },
                    {
                        "attribute": item.product.search_description,
                        "name": "search_description",
                        "type": "label"
                    },
                    {
                        "attribute": item.product.engraving,
                        "name": "product_engraving",
                        "type": "label"
                    },
                    {
                        "attribute": item.product.color,
                        "name": "product_color",
                        "type": "label"
                    },
                    {
                        "attribute": item.quantity,
                        "name": "item_quantity",
                        "type": "input"
                    },
                    {
                        "attribute": item.inventory.id,
                        "name": "inventory_id",
                        "type": "hidden"
                    }
                ])

            return queryset
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(ProductInventoryView, self).get_context_data(**kwargs)
        context['title'] = self.inventory_name
        context['table_headers'] = ['SKU', 'Descripción', 'Descripción para búsqueda', 'Grabado', 'Color', 'Cantidad']
        context['site_title'] = AdminSite.site_title
        context['site_header'] = AdminSite.site_header
        context['app_list'] = reverse('admin:app_list', args=('inventories',))
        context['inventory_list_url'] = reverse('admin:inventories_productsinventory_changelist')
        context['product_inv_item_api_url'] = reverse('productinventoryitem-list')

        return context


class MaterialInventoryView(ListView):
    """
    Class view that generates the HTTP responses for all material inventories
    requests.
    """
    template_name = 'inventories/inventory.html'
    context_object_name = 'inventory_items'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.primary_key = 0
        self.inventory_name = "Inventario de materiales"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.primary_key = kwargs['pk']
        return super(MaterialInventoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        materials_inventory = MaterialsInventory.objects.filter(pk=self.primary_key).first()

        if materials_inventory is not None:
            self.inventory_name = materials_inventory.name
            inventory_items = materials_inventory.materialinventoryitem_set.all()
            queryset = []

            for item in inventory_items:
                queryset.append([
                    item.material.name,
                    item.material.description,
                    item.material.color,
                    item.quantity
                ])

            return queryset
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(MaterialInventoryView, self).get_context_data(**kwargs)
        context['title'] = self.inventory_name
        context['table_headers'] = ['Nombre', 'Descripción', 'Color', 'Cantidad']
        context['site_title'] = AdminSite.site_title
        context['site_header'] = AdminSite.site_header
        context['app_list'] = reverse('admin:app_list', args=('inventories',))
        context['inventory_list_url'] = reverse('admin:inventories_materialsinventory_changelist')

        return context


class ConsumableInventoryView(ListView):
    """
    Class view that generates the HTTP responses for all consumable inventories
    requests.
    """
    template_name = 'inventories/inventory.html'
    context_object_name = 'inventory_items'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.primary_key = 0
        self.inventory_name = "Inventario de consumibles"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.primary_key = kwargs['pk']
        return super(ConsumableInventoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        consumables_inventory = ConsumablesInventory.objects.filter(pk=self.primary_key).first()

        if consumables_inventory is not None:
            self.inventory_name = consumables_inventory.name
            inventory_items = consumables_inventory.consumableinventoryitem_set.all()
            queryset = []

            for item in inventory_items:
                queryset.append([
                    item.consumable.name,
                    item.consumable.description,
                    item.consumable.brand,
                    item.consumable.model,
                    item.quantity
                ])

            return queryset
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(ConsumableInventoryView, self).get_context_data(**kwargs)
        context['title'] = self.inventory_name
        context['table_headers'] = ['Nombre', 'Descripción', 'Marca', 'Modelo', 'Cantidad']
        context['site_title'] = AdminSite.site_title
        context['site_header'] = AdminSite.site_header
        context['app_list'] = reverse('admin:app_list', args=('inventories',))
        context['inventory_list_url'] = reverse('admin:inventories_consumablesinventory_changelist')

        return context


class DurableGoodInventoryView(ListView):
    """
    Class view that generates the HTTP responses for all durable goods inventories
    requests.
    """
    template_name = 'inventories/inventory.html'
    context_object_name = 'inventory_items'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.primary_key = 0
        self.inventory_name = "Inventario de activos"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.primary_key = kwargs['pk']
        return super(DurableGoodInventoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        durable_goods_inventory = DurableGoodsInventory.objects.filter(pk=self.primary_key).first()

        if durable_goods_inventory is not None:
            self.inventory_name = durable_goods_inventory.name
            inventory_items = durable_goods_inventory.durablegoodinventoryitem_set.all()
            queryset = []

            for item in inventory_items:
                queryset.append([
                    item.durable_good.name,
                    item.durable_good.description,
                    item.durable_good.brand,
                    item.durable_good.model,
                    item.quantity
                ])

            return queryset
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(DurableGoodInventoryView, self).get_context_data(**kwargs)
        context['title'] = self.inventory_name
        context['table_headers'] = ['Nombre', 'Descripción', 'Marca', 'Modelo', 'Cantidad']
        context['site_title'] = AdminSite.site_title
        context['site_header'] = AdminSite.site_header
        context['app_list'] = reverse('admin:app_list', args=('inventories',))
        context['inventory_list_url'] = reverse('admin:inventories_durablegoodsinventory_changelist')

        return context


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the Product entity.
    It's used to generate an autocomplete text input in the ProductTransfer
    Add or Change form.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        if self.q:
            search_terms = self.q.split(',')
            search_terms_queries = reduce(operator.and_,
                                          (Q(search_description__icontains=x.strip()) for x in search_terms))
            query_set = Product.objects.filter(search_terms_queries | Q(sku=self.q))
        else:
            query_set = Product.objects.all()

        return query_set


class MaterialAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the Material entity.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Material.objects.none()

        if self.q:
            search_terms = self.q.split(',')
            search_terms_queries = reduce(operator.or_, (Q(description__icontains=x.strip()) for x in search_terms))
            query_set = Material.objects.filter(search_terms_queries)
        else:
            query_set = Material.objects.all()

        return query_set


class ConsumableAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the Consumable entity.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Consumable.objects.none()

        if self.q:
            search_terms = self.q.split(',')
            search_terms_queries = reduce(operator.or_, (Q(description__icontains=x.strip()) for x in search_terms))
            query_set = Consumable.objects.filter(search_terms_queries)
        else:
            query_set = Consumable.objects.all()

        return query_set


class DurableGoodAutocomplete(autocomplete.Select2QuerySetView):
    """
    Select2 framework's autocomplete for the DurableGood entity.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return DurableGood.objects.none()

        if self.q:
            search_terms = self.q.split(',')
            search_terms_queries = reduce(operator.or_, (Q(description__icontains=x.strip()) for x in search_terms))
            query_set = DurableGood.objects.filter(search_terms_queries)
        else:
            query_set = DurableGood.objects.all()

        return query_set


class ProductInventoryItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows a products inventory's item to be viewed or
    edited through a RESTful API.
    """
    queryset = ProductInventoryItem.objects.all()
    serializer_class = ProductInventoryItemSerializer
