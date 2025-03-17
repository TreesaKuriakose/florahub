from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('register_view',views.register_view,name="register_view"),
    path('login_view',views.login_view,name="login_view"),
    path('register',views.register,name="register"),
    path('login1',views.login1,name="login1"),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('home',views.home,name="home"),
    path('plants/', views.plant_list, name='plant_list'), 
    path('forget_password/', views.forget_password, name='forget_password'), 
    path('cart_view/', views.cart_view, name='cart_view'),
    path('cart/add/<int:plant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout_view/', views.checkout_view, name='checkout_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment_view'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('product_list',views.product_list,name="product_list"),
    path('orders/', views.orders_list, name='orders_list'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    
      

    
]
