from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from simple_history.models import HistoricalRecords

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def is_low_stock(self):
        total_qty = self.stocks.aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        return total_qty <= self.reorder_level

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('product', 'location')

    def __str__(self):
        return f"{self.product.name} @ {self.location.name}: {self.quantity}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('TRANSFER', 'Transfer'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    source_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='source_transactions')
    destination_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='destination_transactions')
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.transaction_type == 'IN':
            if not self.destination_location:
                raise ValueError("Destination location required for IN transaction")
            stock, created = Stock.objects.get_or_create(
                product=self.product,
                location=self.destination_location,
                defaults={'quantity': 0}
            )
            stock.quantity += self.quantity
            stock.save()
        elif self.transaction_type == 'OUT':
            if not self.source_location:
                raise ValueError("Source location required for OUT transaction")
            stock = Stock.objects.get(product=self.product, location=self.source_location)
            if stock.quantity < self.quantity:
                raise ValueError("Insufficient stock")
            stock.quantity -= self.quantity
            stock.save()
        elif self.transaction_type == 'TRANSFER':
            if not self.source_location or not self.destination_location:
                raise ValueError("Both source and destination required for transfer")
            source_stock = Stock.objects.get(product=self.product, location=self.source_location)
            if source_stock.quantity < self.quantity:
                raise ValueError("Insufficient stock at source")
            source_stock.quantity -= self.quantity
            source_stock.save()
            dest_stock, created = Stock.objects.get_or_create(
                product=self.product,
                location=self.destination_location,
                defaults={'quantity': 0}
            )
            dest_stock.quantity += self.quantity
            dest_stock.save()
        super().save(*args, **kwargs)