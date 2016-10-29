import logging
import operator
from functools import reduce

from dal import autocomplete
from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import View
from rest_framework import viewsets

from inventories.forms.solver_forms import SolverForm
from inventories.models import ProductsInventory, MaterialsInventory, ConsumablesInventory, DurableGoodsInventory, \
    Product, Material, Consumable, DurableGood, ProductInventoryItem, string_to_model_class
from inventories.serializers import ProductInventoryItemSerializer
from inventories.solver import Surface, ProductCutOptimizer

db_logger = logging.getLogger('db')


class ProductSolverView(View):
    """
    The view for the solver.
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
        try:
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
        except Exception as e:
            db_logger.exception(e)
            raise


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
                                          (Q(search_description__icontains=x.strip())
                                           for x in search_terms))
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


class ProductMovementConfirmOrCancelView(View):
    """
    This view is used to confirm or cancel one of three different models:
    PurchaseOrder, ProductEntry or ProductRemoval.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductMovementConfirmOrCancelView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Responds to POST requests.
        This view is used to confirm or cancel one of three different models:
        PurchaseOrder, ProductEntry or ProductRemoval. The model's class name
        is provided in the request, along with the primary key and the action
        to perform: confirmation or cancellation.
        :param request: The HTTP request.
        :return: A JSON response.
        """
        try:
            model_class = string_to_model_class(request.POST.get('model'))
            obj = get_object_or_404(model_class, pk=request.POST.get('pk'))
            action = request.POST.get('action')

            if not model_class or not obj or not action:
                raise Exception("El servidor no recibió los parámetros esperados.")

            obj.confirmed_by_user = request.user

            if action == "confirm":
                obj.confirm()
                success = obj.status == model_class.STATUS_CONFIRMED
                message = obj.ajax_message_for_confirmation
            elif action == "cancel":
                obj.cancel()
                success = obj.status == model_class.STATUS_CANCELLED
                message = obj.ajax_message_for_cancellation

            return JsonResponse({'success': success, 'message': message})
        except Exception as e:
            db_logger.exception(e)
            return JsonResponse({'success': False, 'message': str(e)})
