from django.contrib import admin
from .models import *

# Myorder


@admin.register(AllOrder)
class AllOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "product",
        "address",
        "ammount",
        "quantity",
        "user",
    )


# !CURRENT ORDER
@admin.register(CurrentOrder)
class CurrentOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orderStatus",
        "product",
        "address",
        "ammount",
        "quantity",
        "user",
    )


# ! SUCCESS ORDERKEY
@admin.register(SuccessOrder)
class SuccessOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orderSeller",
        "product",
        "address",
        "quantity",
        "user",
    )


# PRDOCUT IN CART
@admin.register(CancelOrder)
class CancelOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "orderUser", "orderSeller", "ammount")


# # LIKE
# @admin.register(AllDataNotification)
# class AllDataNotiAdmin(admin.ModelAdmin):
#     list_display = ("id", "orderkey", "user", "addresskey")


# # NOTIFICATIONS
# @admin.register(NotificationOrder)
# class OrderNotificationAdmin(admin.ModelAdmin):
#     list_display = ("id", "product", "sender", "status", "date", "is_seen", "txt")
