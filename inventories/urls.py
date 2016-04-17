from django.conf.urls import url
from inventories import views

urlpatterns = [
    url(r'^product/(?P<pk>\d+)/$', views.ProductInventoryView.as_view()),
]
