from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Location, Category, Product, Stock, Transaction

@admin.register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ('sku', 'name', 'category', 'unit_price', 'reorder_level')
    list_filter = ('category',)
    search_fields = ('sku', 'name')

@admin.register(Stock)
class StockAdmin(SimpleHistoryAdmin):
    list_display = ('product', 'location', 'quantity')
    list_filter = ('location',)

@admin.register(Transaction)
class TransactionAdmin(SimpleHistoryAdmin):
    list_display = ('product', 'transaction_type', 'quantity', 'date', 'user')
    list_filter = ('transaction_type', 'date')
    search_fields = ('product__name',)