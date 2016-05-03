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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from finances import views
from inventories import urls as inventories_urls
from inventories.views import ProductAutocomplete
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
    url(r'^product-autocomplete/$', ProductAutocomplete.as_view(), name='product-autocomplete', ),
]
