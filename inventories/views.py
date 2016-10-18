import operator
from functools import reduce

from dal import autocomplete
from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import View
from rest_framework import viewsets

from back_office.models import EmployeeGroup
from inventories.forms.solver_forms import SolverForm
from inventories.models import ProductsInventory, MaterialsInventory, ConsumablesInventory, DurableGoodsInventory, \
    Product, Material, Consumable, DurableGood, ProductInventoryItem, ProductRemoval
from inventories.serializers import ProductInventoryItemSerializer
from inventories.solver import Surface, ProductCutOptimizer


class ProductSolverView(View):
    """

    """
    form_class = SolverForm
    template_name = 'inventories/solver.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductSolverView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class ProductSolverResultView(View):
    form_class = SolverForm
    template_name = 'inventories/solver_result.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductSolverResultView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request.GET)

        if form.is_valid():
            inventory = request.user.branch_office.productsinventory

            solver = ProductCutOptimizer(
                inventory=inventory,
                surface_area=Surface(width=form.cleaned_data['width'],
                                     length=form.cleaned_data['length']),
                product_lines=form.cleaned_data['product_lines'],
                quantity=form.cleaned_data['quantity']
            )

            products, remaining = solver.get_candidate_products_for_surface()

            return render(request, self.template_name, {
                'products': products,
                'remaining': remaining,
                'inventory': inventory,
                'width': form.cleaned_data['width'],
                'length': form.cleaned_data['length'],
                'quantity': form.cleaned_data['quantity'],
                'product_lines': ", ".join(
                    [x[1] for x in Product.LINE_TYPES if str(x[0]) in form.cleaned_data['product_lines']]),
            })
        else:
            return HttpResponseBadRequest()


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


class ProductRemovalReviewView(View):
    """
    View that accepts a ProductRemoval and removes its related products from the
    current user's inventory.
    """

    def __init__(self, *args, **kwargs):
        self.updated_values = []
        self.errors = []
        super(ProductRemovalReviewView, self).__init__(*args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductRemovalReviewView, self).dispatch(request, *args, **kwargs)

    def post(self, request, product_removal_id):
        success = False
        product_removal = get_object_or_404(ProductRemoval, pk=product_removal_id)
        inventory = request.user.branch_office.productsinventory
        action = request.GET.get('action')

        if not self.is_user_valid(request.user):
            self.errors.append("Sólo un Jefe de Almacén puede realizar esta acción.")
            success = False
        elif action == 'confirm':
            self.validate_products_in_inventory(inventory, product_removal)

            success = False if any(self.errors) else True

            if success:
                self.decrease_inventory_for_removed_products(inventory, product_removal)
                product_removal.status = ProductRemoval.STATUS_CONFIRMED
                ProductRemoval.save()
        elif action == 'cancel':
            success = True
            product_removal.status = ProductRemoval.STATUS_CANCELLED
            product_removal.save()

        return JsonResponse({'success': success, 'errors': self.errors, 'updated_values': self.updated_values,
                             'product_removal_status': product_removal.status})

    @staticmethod
    def is_user_valid(user):
        """
        Specified is the given user may perfom the actions in this view.
        :param user: The user to validate.
        :return: True if it can, False otherwise.
        """
        if user.is_superuser:
            is_valid = True
        if EmployeeGroup.WAREHOUSE_CHIEF not in user.groups.all():
            is_valid = False

        return is_valid

    def decrease_inventory_for_removed_products(self, inventory, product_removal):
        """
        For each product in the product removal, its quantity is decreased from the
        corresponding product inventory item.
        :param inventory: The inventory from which the products are removed.
        :param product_removal: The removal from whose products are the source for the
        removal.
        """
        with transaction.atomic():
            for removed_product in product_removal.removedproduct_set.all():
                product_inventory_item = inventory.productinventoryitem_set.filter(
                    product=removed_product.product
                ).first()

                old_quantity = product_inventory_item.quantity
                new_quantity = product_inventory_item.quantity - removed_product.quantity
                product_inventory_item.quantity = new_quantity
                product_inventory_item.save()

                self.updated_values.append({
                    'product': str(removed_product.product),
                    'old_quantity': str(old_quantity),
                    'new_quantity': str(new_quantity)
                })

    def validate_products_in_inventory(self, inventory, product_removal):
        """
        Determines if there are any errors with the products to be removed
        and the current user's inventory. If there are any, the errors member
        is updated.
        :param inventory: The current user's inventory.
        :param product_removal: The set of products to be removed.
        """
        for removed_product in product_removal.removedproduct_set.all():
            product_inventory_item = inventory.productinventoryitem_set.filter(
                product=removed_product.product
            ).first()

            if product_inventory_item is None:
                self.errors.append("El producto {0} no existe en el inventario {1}. Hay que agregarlo.".format(
                    str(removed_product.product), str(inventory)
                ))

                continue

            if product_inventory_item.quantity < removed_product.quantity:
                self.errors.append("{0} sólo cuenta con {1} unidades del producto {2}.".format(
                    str(inventory), str(product_inventory_item.quantity), str(removed_product.product)
                ))

                continue
