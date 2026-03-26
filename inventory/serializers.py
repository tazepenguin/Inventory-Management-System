from rest_framework import serializers
from .models import Product, Stock, Transaction

class ProductSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'description', 'unit_price', 'reorder_level', 'total_quantity']

    def get_total_quantity(self, obj):
        return obj.stocks.aggregate(serializers.models.Sum('quantity'))['quantity__sum'] or 0

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    class Meta:
        model = Stock
        fields = ['id', 'product', 'product_name', 'location', 'location_name', 'quantity']

class TransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    source_location_name = serializers.CharField(source='source_location.name', read_only=True)
    destination_location_name = serializers.CharField(source='destination_location.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['date', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)