from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from django.db.models import Sum
from .models import Product, Transaction, Location, Category, Stock
from .forms import ProductForm, TransactionForm
import json

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    low_stock_products = [p for p in Product.objects.all() if p.is_low_stock()]
    recent_transactions = Transaction.objects.select_related('product').order_by('-date')[:10]

    stock_by_location = []
    locations = Location.objects.filter(is_active=True)
    for loc in locations:
        total = Stock.objects.filter(location=loc).aggregate(Sum('quantity'))['quantity__sum'] or 0
        stock_by_location.append({'location': loc.name, 'quantity': total})

    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'recent_transactions': recent_transactions,
        'stock_by_location_json': json.dumps(stock_by_location),
    }
    return render(request, 'inventory/dashboard.html', context)

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(sku__icontains=search)
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory.add_product'

    def form_valid(self, form):
        messages.success(self.request, "Product added successfully.")
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory.change_product'

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully.")
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory.delete_product'

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Product deleted.")
        return super().delete(request, *args, **kwargs)

class TransactionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'inventory/transaction_form.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'inventory.add_transaction'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Transaction recorded.")
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        return response

@login_required
@permission_required('inventory.view_report', raise_exception=True)
def export_products_csv(request):
    import csv
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['SKU', 'Product Name', 'Category', 'Total Quantity', 'Unit Price', 'Total Value'])
    products = Product.objects.all()
    for p in products:
        total_qty = p.stocks.aggregate(Sum('quantity'))['quantity__sum'] or 0
        writer.writerow([p.sku, p.name, p.category.name if p.category else '', total_qty, p.unit_price, total_qty * p.unit_price])
    return response

@login_required
def stock_by_location_report(request):
    data = []
    locations = Location.objects.filter(is_active=True)
    for loc in locations:
        total_qty = Stock.objects.filter(location=loc).aggregate(Sum('quantity'))['quantity__sum'] or 0
        data.append({'location': loc.name, 'quantity': total_qty})
    return render(request, 'inventory/reports/stock_by_location.html', {'data': json.dumps(data)})