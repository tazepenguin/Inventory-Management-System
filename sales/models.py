from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product, Location
from simple_history.models import HistoricalRecords
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class SalesOrder(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('CONFIRMED', 'Confirmed'),
        ('FULFILLED', 'Fulfilled'),
        ('CANCELLED', 'Cancelled'),
    )
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fulfilled_from_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.order_number:
            today = timezone.now().strftime('%Y%m%d')
            last_order = SalesOrder.objects.filter(order_number__startswith=f'ORD-{today}').order_by('-order_number').first()
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.order_number = f'ORD-{today}-{new_num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.order.total_amount = sum(item.total_price for item in self.order.items.all())
        self.order.save()

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"