from django.db import models
import requests
import json
# Create your models here.
class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200, default="No name")
    price = models.FloatField(default=0.00)
    stock = models.IntegerField(default=0)

class Order(models.Model):
    date_time = models.DateTimeField(blank=True)
    products = models.ManyToManyField(Product,through="OrderDetail", blank=True, related_name="prodsOrder")
    def computeTotal(self):
        total = 0
        details = OrderDetail.objects.filter(order=self)
        for detail in details:
            prodInstance = Product.objects.filter(id=detail.product.id).first()
            total = total + (detail.quantity*prodInstance.price)
        return total
    @property
    def get_total(self):
        return self.computeTotal()
    @property
    def get_total_usd(self):
        externalResponse = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        resp_status = externalResponse.status_code
        influx = externalResponse.json()
        dolarPrice = str(influx[1]["casa"]["compra"]).replace(",",".")
        dolarPrice = float(dolarPrice)
        return self.computeTotal()*dolarPrice
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)


