from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .manager import CustomUserManager
import uuid
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password



# MY CUSTOMUSER
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    phone = models.CharField(
        unique=True, max_length=15, validators=[RegexValidator("^[789]\d{9}$")]
    )
    fullname = models.CharField(
        _("full name"),
        max_length=130,
    )
    country_code = models.IntegerField(default=91)
    email = models.EmailField(_("emailaddress"), unique=True)
    is_staff = models.BooleanField(_("is_staff"), default=False)
    is_active = models.BooleanField(_("is_active"), default=True)
    date_joined = models.DateField(_("date_joined"), default=date.today)
    change_pw = models.BooleanField(default=True)
    isCustomer = models.BooleanField(default=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = [
        "fullname",
    ]

    objects = CustomUserManager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("Accounts")
        verbose_name_plural = _("Acconts")

    def get_short_name(self):
        """
        Returns the display name.
        If full name is present then return full name as display name
        else return username.
        """
        if self.fullname != "":
            return self.fullname
        else:
            return str(self.phone)


# Profile for all
class Profile(models.Model):
    id = models.UUIDField(
        primary_key=True,
    )
    fullname = models.CharField(max_length=100)
    email = models.EmailField(_("emailaddress"), unique=True, null=True, blank=True)
    uplod = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
        max_length=200,
        null=True,
        blank=True,
    )
    pic = models.ImageField(upload_to="CustomerImg", blank=True, null=True)

    # @permalink
    def get_absolute_url(self):
        return reverse("", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.uplod.id)


# ADDRESS
STATE_CHOICES = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu & Kashmir", "Jammu & Kashmir"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram ", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
)

Dtime = (
    ("Home (7 am - 9 pm delivery)", "Home (7 am - 9 pm delivery)"),
    ("Office (10 am - 6 pm delivery)", "Office (10 am - 6 pm delivery)"),
    ("AnyTime", "AnyTime"),
)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uplod = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="addressuser"
    )
    fullname = models.CharField(
        _("full name"),
        max_length=130,
    )
    phone = models.CharField(max_length=15, validators=[RegexValidator("^[789]\d{9}$")])
    email = models.EmailField(_("emailaddress"), null=True, blank=True)
    house = models.CharField(max_length=300, null=True, blank=True)
    trade = models.CharField(max_length=200, null=True, blank=True)
    area = models.CharField(max_length=200,  null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pinCode = models.CharField(
        max_length=100,
        validators=[RegexValidator("^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")],
    )
    delTime = models.CharField(max_length=100, choices=Dtime, default="AnyTime")
    state = models.CharField(choices=STATE_CHOICES, max_length=200, )
    

    def __str__(self):
        return str(self.uplod)
