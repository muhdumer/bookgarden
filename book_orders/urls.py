from django.urls import path
from .views import CheckoutOrderView,getAddressObject,OrderListView,OrderDetailView

app_name='order_app'


urlpatterns = [
    path('checkout/',CheckoutOrderView,name='checkout-order'),
    path('checkout/getAddress/',getAddressObject,name='get_address_object'),
    path('orderlist/',OrderListView.as_view(),name='order_list'),
    path('<int:pk>/orderdetail/',OrderDetailView.as_view(),name='order_detail')
]
