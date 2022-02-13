from rest_framework import serializers
from .signals import *
from .models import *
class ProductSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Product
        fields = "__all__"
class OrderDetailSerializer(serializers.ModelSerializer):
    def validate(self, value):
        ODInstance = self.instance
        print(value["product"])
        productInstance = Product.objects.filter(id=value["product"].id).first()
        if(value["quantity"]>productInstance.stock):
            raise serializers.ValidationError("Insufficient stock for product ", (productInstance.id))
        return value  
    class Meta:
        model = OrderDetail
        fields = "__all__"
class OrderSerializer(serializers.ModelSerializer):
    productsDetail = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    total_usd = serializers.SerializerMethodField()
    def validate(self, value):
        reqMethod = self.context["request"].method
        payloadProds = self.context["products"]
        payloadQuants = self.context["quantities"]
        prunedPayloadProducts = set(payloadProds)
        #Check if duplicate JSON data was sent...
        if(len(prunedPayloadProducts) != len(payloadProds)):
            raise serializers.ValidationError("Repeated product info sent")
        negatives = [x for x in payloadQuants if x <=0]
        if(len(negatives)!=0):
            raise serializers.ValidationError("Zero quantitiy is not allowed")
    def create(self,validated_data):
        instance = Order.objects.create(**validated_data)
        for i, productId in enumerate(self.context["products"]):
            prodIns = Product.objects.filter(id=productId).first()
            ODInstance = OrderDetail.objects.create(order=instance, quantity=self.context["quantities"][i], product=prodIns)
        return instance
    def update(self, instance, validated_data): 
        instance.date_time = validated_data.get('date_time', instance.date_time)
        newProducts = self.context["products"]
        newQuantities = self.context["quantities"]
        for i, productId in enumerate(newProducts):
            prodInstance = Product.objects.filter(id=productId).first()
            newQuant = newQuantities[i]
            ODInstance = OrderDetail.objects.filter(order=instance, product=prodInstance).first()
            if(ODInstance!=None):
                oldQuant = ODInstance.quantity
                ODInstance = OrderDetailSerializer(ODInstance, data={"order":instance.id, "quantity": newQuant, "product":prodInstance.id})
            else:
                oldQuant = 0
                ODInstance = OrderDetailSerializer(data={"order":instance.id, "quantity": newQuant, "product":prodInstance.id})
            ODInstance.is_valid()
            print("Old:", oldQuant)
            print("New:", newQuant)
            stockDifference = oldQuant - newQuant
            print("Cambio en stock: ", stockDifference)
            prodInstance.stock = prodInstance.stock + stockDifference
            prodInstance.save()
            ODInstance.validated_data["quantity"] = newQuant 
            ODInstance.is_valid()
            ODInstance.save()
        return instance
    def get_productsDetail(self, instance):
        productsDetails = OrderDetail.objects.filter(order=instance)
        return OrderDetailSerializer(productsDetails, many=True).data
    def get_total(self, obj):
        return obj.get_total
    def get_total_usd(self, obj):
        return obj.get_total_usd
    class Meta:
        model = Order
        fields = ("id","date_time","productsDetail","total","total_usd")
    

