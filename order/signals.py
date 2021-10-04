from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import *
from accounts.models import *

# # ! CURRENT ORDER
# @receiver(post_save, sender=AllOrder)
# def add_to_order(sender, instance, *arg, **kwargs):

#     if instance.status == "Accept" or instance.status == "Pending":
#         var, created = CurrentOrder.objects.update_or_create(
#             # ! data for checking that id is exit or not
#             orderSeller=instance,
#             id=instance.id,
#             product=instance.product,
#             user=instance.user,
#             # ! value for update
#             defaults={
#                 "address": instance.address,
#                 "ammount": instance.ammount,
#                 # "amount": 1000,
#                 "quantity": instance.quantity,
#             },
#         )
#     elif instance.status == "Decline":
#         var, created = CancelOrder.objects.update_or_create(
#             # ! data for checking that id is exit or not
#             orderSeller=instance,
#             id=instance.id,
#             product=instance.product,
#             user=instance.user,
#             # ! value for update
#             defaults={
#                 "address": instance.address,
#                 "ammount": instance.ammount,
#                 # "amount": 1000,
#                 "quantity": instance.quantity,
#             },
#         )
#         curOd = CurrentOrder.objects.filter(
#             orderSeller=instance,
#             id=instance.id,
#             product=instance.product,
#             user=instance.user,
#         ).delete()


# # addtocart
# @receiver(post_save,sender=AllOrder)
# def add_to_order(sender,instance,created,*arg,**kwargs):
#     like=instance
#     # product=like.product
#     # sender=like.customer_cart
#     # print('==================================')
#     # print("add in  LIKE  " ,like)
#     # print("add in  product  " ,instance.product)
#     # print("add in  sender " ,instance.user)
#     # print('uplod in d' ,instance.product.uplod)
#     # print('status ' ,instance.status)
#     # if created:
#     notifty=NotificationOrder(product=instance.product,sender=instance.user,user=instance.product.uplod,status=instance.status)
#     notifty.save()
#     print("add in  order ")
#     if instance.status == 'Shipment':
#         print('check then caleu')


# @receiver(post_save,sender=AllOrder)
# def user_Cancel(sender,instance, created,*arg,**kwargs):

#     if instance.status == 'Decline':
#         if created:
#          notifty=CancelOrder.objects.update_or_create(id=instance.id,product=instance.product,user=instance.user,status='Decline')

#         print("add in candel order ")
