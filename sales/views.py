from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from .models import Customer, SalesOrder, OrderItem
from .forms import CustomerForm, SalesOrderForm, OrderItemForm
from inventory.models import Location, Transaction

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer created.")
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/customer_form.html', {'form': form})

@login_required
def order_list(request):
    orders = SalesOrder.objects.select_related('customer').all()
    return render(request, 'sales/order_list.html', {'orders': orders})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            return redirect('order_edit', pk=order.pk)
    else:
        form = SalesOrderForm()
    return render(request, 'sales/order_form.html', {'form': form})

@login_required
def order_edit(request, pk):
    order = get_object_or_404(SalesOrder, pk=pk)
    items = order.items.all()
    if request.method == 'POST':
        if 'add_item' in request.POST:
            item_form = OrderItemForm(request.POST)
            if item_form.is_valid():
                item = item_form.save(commit=False)
                item.order = order
                item.save()
                messages.success(request, "Item added.")
                return redirect('order_edit', pk=order.pk)
        elif 'confirm' in request.POST:
            if order.items.count() == 0:
                messages.error(request, "Cannot confirm empty order.")
            else:
                order.status = 'CONFIRMED'
                order.save()
                messages.success(request, "Order confirmed.")
                return redirect('order_list')
        elif 'cancel' in request.POST:
            order.status = 'CANCELLED'
            order.save()
            messages.success(request, "Order cancelled.")
            return redirect('order_list')
        elif 'fulfill' in request.POST:
            location_id = request.POST.get('location')
            if not location_id:
                messages.error(request, "Select a fulfillment location.")
            else:
                try:
                    location = Location.objects.get(id=location_id)
                    for item in items:
                        stock = item.product.stocks.filter(location=location).first()
                        if not stock or stock.quantity < item.quantity:
                            messages.error(request, f"Insufficient stock for {item.product.name} at {location.name}")
                            break
                    else:
                        for item in items:
                            Transaction.objects.create(
                                product=item.product,
                                transaction_type='OUT',
                                quantity=item.quantity,
                                source_location=location,
                                user=request.user,
                                notes=f"Fulfilling order {order.order_number}"
                            )
                        order.status = 'FULFILLED'
                        order.fulfilled_from_location = location
                        order.fulfilled_at = timezone.now()
                        order.save()
                        messages.success(request, "Order fulfilled.")
                        return redirect('order_list')
                except Location.DoesNotExist:
                    messages.error(request, "Invalid location.")
    else:
        item_form = OrderItemForm()
    locations = Location.objects.filter(is_active=True)
    return render(request, 'sales/order_edit.html', {'order': order, 'items': items, 'item_form': item_form, 'locations': locations})