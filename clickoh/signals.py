
from clickoh.models import *
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django import dispatch
@receiver(post_save, sender=OrderDetail)
def order_creation_stock(sender, instance, created, **kwargs):
    if created:
        productInstance = Product.objects.filter(id=instance.product.id).first()
        productInstance.stock = productInstance.stock - instance.quantity
        productInstance.save()
@receiver(pre_delete, sender=OrderDetail)
def restore_stock(sender, instance,**kwargs):
    productInstance = Product.objects.filter(id=instance.product.id).first()
    productInstance.stock = productInstance.stock + instance.quantity
    productInstance.save()



