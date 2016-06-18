"""Acriladmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from back_office.views import AddressAutocomplete, ClientAutocomplete
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from finances import views
from finances.views import InvoiceAutocomplete
from inventories import urls as inventories_urls
from inventories.views import ProductAutocomplete, MaterialAutocomplete, ConsumableAutocomplete, DurableGoodAutocomplete
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'finances/productprice', views.ProductPriceViewSet)
router.register(r'finances/materialcost', views.MaterialCostViewSet)

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^inventories/', include(inventories_urls)),
    url(r'^select2/', include('django_select2.urls')),
    url(r'session_security/', include('session_security.urls')),
    url(r'^product-autocomplete/$', ProductAutocomplete.as_view(), name='product-autocomplete', ),
    url(r'^material-autocomplete/$', MaterialAutocomplete.as_view(), name='material-autocomplete', ),
    url(r'^consumable-autocomplete/$', ConsumableAutocomplete.as_view(), name='consumable-autocomplete', ),
    url(r'^durablegood-autocomplete/$', DurableGoodAutocomplete.as_view(), name='durablegood-autocomplete', ),
    url(r'^address-autocomplete/$', AddressAutocomplete.as_view(), name='address-autocomplete', ),
    url(r'^client-autocomplete/$', ClientAutocomplete.as_view(), name='client-autocomplete', ),
    url(r'^invoice-autocomplete/$', InvoiceAutocomplete.as_view(), name='invoice-autocomplete', ),
]
