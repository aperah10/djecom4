from rest_framework import serializers

# MY IMPORT FOR ALL FIELS
from accounts.models import *
from product.models import *
from order.models import *

# ================

# make accounts in
class AccountsSeri(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "fullname", "phone", "password"]

        def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            # Token.objects.create(user=user)
            return user


# ---------------------------------------------------------------------------- #
#                    orc ProfilePage GET AND POST SERILIZER                    #
# ---------------------------------------------------------------------------- #

# ! PROFILE POST METHOD
class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "fullname",
            "email",
            "pic",
            "gender",
        ]


# ---------------------------------------------------------------------------- #
#                       ! ADDRESS METHOD POST AND GET SERILIZER                                         #
# ---------------------------------------------------------------------------- #
class AddressSer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class PostAddressSer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "fullname",
            "phone",
            "email",
            "house",
            "trade",
            "area",
            "city",
            "pinCode",
            "delTime",
            "state",
            "uplod",
        ]


# ALL PRODUCT SHOW DATA
class AllProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1
# ---------------------------------------------------------------------------- #
#                           orc CART ADDED SERILIZER                           #
# ---------------------------------------------------------------------------- #

# CART FOR DATA
class CartSer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = "__all__"
        depth = 2

class AddCartSer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = ["product", "quantity", "uplod"]

class UpCartSer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = [ "quantity",]

# ! ORDER PAGE METHOD
class AllOrderSer(serializers.ModelSerializer):
    class Meta:
        model = AllOrder
        fields = ['quantity','address','uplod','product']
        # depth = 2


class CurrentOrderSer(serializers.ModelSerializer):
    class Meta:
        model = CurrentOrder
        fields = "__all__"
        # depth = 2
