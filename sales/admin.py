from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Customer, SalesOrder, OrderItem

@admin.register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'email', 'phone')

@admin.register(SalesOrder)
class SalesOrderAdmin(SimpleHistoryAdmin):
    list_display = ('order_number', 'customer', 'order_date', 'status', 'total_amount')
    list_filter = ('status', 'order_date')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'total_price')