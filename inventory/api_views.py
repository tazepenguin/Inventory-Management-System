from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Product, Stock, Transaction
from .serializers import ProductSerializer, StockSerializer, TransactionSerializer
from .permissions import IsAdminOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['sku', 'name']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_products = [p for p in Product.objects.all() if p.is_low_stock()]
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('product', 'location')
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name', 'location__name']

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related('product', 'source_location', 'destination_location', 'user')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)