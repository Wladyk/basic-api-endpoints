from rest_framework import routers
from clickoh import viewsets
router = routers.DefaultRouter()
router.register(r'product', viewsets.ProductViewset, basename="product")
router.register(r'order', viewsets.OrderViewset, basename="order")
