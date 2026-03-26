from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'stocks', api_views.StockViewSet)
router.register(r'transactions', api_views.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]