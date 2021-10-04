from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import *
from django.db.models import Q

# # addtocart
# @receiver(post_save, sender=ProductCart)
# def add_to_cart(sender, instance, created, *arg, **kwargs):
#     print(instance.customerCart)
#     cart=ProductCart.objects.filter(Q(customerCart=instance.customerCart)& Q(id=instance.id))
    
#     if cart:
#         print('yes is work')
#         cart.update(quantity= instance.quantity,ammount= instance.ammount,shipPrice= instance.shipPrice,
#                 totalAmmount= instance.totalAmmount,)
                
            
        



