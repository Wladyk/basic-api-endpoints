from rest_framework import viewsets, status
from clickoh.models import *
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ProductViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()

class OrderViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    def create(self, request):
        p_Date = request.data.get('date_time')
        p_Details = request.data.get('details')
        quantities = []
        productsIds = []
        for elem in p_Details:
            productsIds.append(elem["productId"])
            quantities.append(elem["quantity"])
        payload = {"date_time" : p_Date}
        serialized = self.get_serializer(data=payload, context={"request": request,"quantities": quantities, "products" : productsIds})
        if(serialized.is_valid()):
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors)
    def destroy(self, request, pk=None):
        instance = Order.objects.filter(id=pk).first()
        OrderDetail.objects.filter(order=instance).delete()
        instance.delete()
        return Response({'success': 'Data destroyed'}, status=status.HTTP_200_OK)
    def update(self, request, pk=None, partial=True):
        instance = Order.objects.filter(id=pk).first()
        p_Date = request.data.get('date_time')
        p_Details = request.data.get('details')
        quantities = []
        productsIds = []
        for elem in p_Details:
            productsIds.append(elem["productId"])
            quantities.append(elem["quantity"])
        payload = {"date_time" : p_Date}
        serialized = self.get_serializer(instance, data=payload, context={"request": request,"quantities": quantities, "products" : productsIds})
        if(serialized.is_valid()):
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors)
    @action(detail=True,methods=['POST'], name='DeleteProduct')
    def deleteProduct(self, request, pk=None):
        targetOrder = Order.objects.filter(id=pk).first()
        targetProduct = Product.objects.filter(id=request.data.get('productId')).first()
        instance = OrderDetail.objects.filter(order=targetOrder, product=targetProduct).first() 
        instance.delete()
        return Response({'success': 'Data destroyed'}, status=status.HTTP_200_OK)
