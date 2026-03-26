from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_add'),
    path('orders/', views.order_list, name='sales_order_list'),
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
]