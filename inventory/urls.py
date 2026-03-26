from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction_add'),
    path('reports/export-csv/', views.export_products_csv, name='export_csv'),
    path('reports/stock-by-location/', views.stock_by_location_report, name='stock_by_location_report'),
]