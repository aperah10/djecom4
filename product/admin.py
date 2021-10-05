from django.contrib import admin
from .models import *

# Register your models here.

# PRODUCT
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uplod",
        "title",
        "description",
        "quantity",
        "ammount",
        "salesPrice",
        "ourPrice",
        "discountPrice",
        "category",
        "date",
        "stock",
        "pic",
        "offers",
    )




@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "uplod",
        "quantity",
        "ammount",
        "totalAmmount"
    )











