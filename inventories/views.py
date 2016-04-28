from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from inventories.models import ProductsInventory, MaterialsInventory, ConsumablesInventory, DurableGoodsInventory


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
            inventory_items = products_inventory.items.all()
            queryset = []

            for item in inventory_items:
                queryset.append([
                    item.product.sku,
                    item.product.name,
                    item.quantity
                ])

            return queryset
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(ProductInventoryView, self).get_context_data(**kwargs)
        context['title'] = self.inventory_name
        context['table_headers'] = ['Imagen', 'SKU', 'Producto', 'Cantidad']
        context['site_title'] = AdminSite.site_title
        context['site_header'] = AdminSite.site_header
        context['app_list'] = reverse('admin:app_list', args=('inventories',))
        context['inventory_list_url'] = reverse('admin:inventories_productsinventory_changelist')

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
            inventory_items = materials_inventory.items.all()
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
        context['table_headers'] = ['Imagen', 'Nombre', 'Descripción', 'Color', 'Cantidad']
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
            inventory_items = consumables_inventory.items.all()
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
        context['table_headers'] = ['Imagen', 'Nombre', 'Descripción', 'Marca', 'Modelo', 'Cantidad']
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
            inventory_items = durable_goods_inventory.items.all()
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
        context['table_headers'] = ['Imagen', 'Nombre', 'Descripción', 'Marca', 'Modelo', 'Cantidad']
        context['site_title'] = AdminSite.site_title
        context['site_header'] = AdminSite.site_header
        context['app_list'] = reverse('admin:app_list', args=('inventories',))
        context['inventory_list_url'] = reverse('admin:inventories_durablegoodsinventory_changelist')

        return context
