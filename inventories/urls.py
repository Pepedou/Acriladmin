from django.conf.urls import url
from inventories import views

urlpatterns = [
    url(r'^product/(?P<pk>\d+)/$', views.ProductInventoryView.as_view()),
    url(r'^material/(?P<pk>\d+)/$', views.MaterialInventoryView.as_view()),
    url(r'^consumable/(?P<pk>\d+)/$', views.ConsumableInventoryView.as_view()),
    url(r'^durable_good/(?P<pk>\d+)/$', views.DurableGoodInventoryView.as_view()),
]
