from django.db import models
import uuid
from accounts.models import *
from product.models import *

# Create your models here.

# ------------------ORDER MODEL ------------------------------
OrderStateT = (
    ("Dispatch", "Dispatch"),
    ("Shipment", "Shipment"),
    ("Arrives at", "Arrives at"),
    ("Complete", "Complete"),
)

StateT = (("Pending", "Pending"), ("Accept", "Accept"), ("Decline", "Decline"))


# ORDER BASE CLASS
class BaseOrder(models.Model):
    uplod = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    ammount = models.PositiveIntegerField()
    shipPrice = models.PositiveIntegerField(default=50)
    totalAmmount = models.PositiveIntegerField(default=0)

    # ! this method add ammount value is
    def save(self, *args, **kwargs):
        if not self.pk:
            self.ammount = self.product.discountPrice * self.quantity
            if self.ammount > 499:
                self.shipPrice = 0
                self.totalAmmount = self.ammount + self.shipPrice
            else:
                self.shipPrice = 70
                self.totalAmmount = self.ammount + self.shipPrice
        else:
            self.ammount = self.product.discountPrice * self.quantity
            if self.ammount > 499:
                self.shipPrice = 0
                self.totalAmmount = self.ammount + self.shipPrice
            else:
                self.shipPrice = 70
                self.totalAmmount = self.ammount + self.shipPrice

        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class AllOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    status = models.CharField(max_length=100, choices=StateT)


# ! CURRENT ORDER
class CurrentOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(AllOrder, on_delete=models.CASCADE)
    orderStatus = models.CharField(
        max_length=100,
        choices=OrderStateT,
        default="OrderConfirm",
        null=True,
        blank=True,
    )


# Success ORDER
class SuccessOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(CurrentOrder, on_delete=models.CASCADE)


# CANCEL ORDER
class CancelOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(
        AllOrder, on_delete=models.CASCADE, null=True, blank=True
    )
    orderUser = models.ForeignKey(
        CurrentOrder, on_delete=models.CASCADE, null=True, blank=True
    )

