from django.db import models
from accounts.models import CustomUser
from django.urls import reverse
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey


# ADD PRODUCT
#  ---------------------ADD PRODUCT --------------------------
Cat = (
    ("Clothes", "Clothes"),
    ("Mobile", "Mobile"),
    ("Beauty", "Beauty"),
    ("Grocery", "Grocery"),
)


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    salesPrice = models.FloatField()
    discountPrice = models.FloatField()
    ourPrice = models.FloatField(blank=True, null=True, default=0)
    category = models.CharField(choices=Cat, max_length=200,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField()
    pic = models.ImageField(upload_to="ProdcutImg", blank=True)
    offers = models.IntegerField(default=1, null=True, blank=True)
    uplod = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)
    ammount = models.PositiveIntegerField(default=0)

    # ! this method add ammount value is
    def save(self, *args, **kwargs):
        if not self.pk:  # Check for create
            self.ammount = self.discountPrice * self.quantity
        else:

            self.ammount = self.discountPrice * self.quantity
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


# !Product Cart
class ProductCart(models.Model):
    class Meta:
        unique_together = (("uplod"), ("product"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uplod = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ammount = models.PositiveIntegerField(default=0)
    shipPrice = models.PositiveIntegerField(default=50)
    totalAmmount = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

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



