from django.urls import path

from .views import products_list, product_detail, search, cart_detail, add_to_cart, remove_from_cart, clear_cart, \
    order_processed

urlpatterns = [
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('category/', products_list, name='products_list'),
    path('category/<slug:slug>/', products_list, name='products_list_by_category'),
    path('search/', search, name='search'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', add_to_cart, name='cart_update'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('cart/orderprocessed/', order_processed, name='order_processed')
]
