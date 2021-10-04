from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from django.views.generic import TemplateView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


# MY IMPORTS FOR ALL FILES
from accounts.models import *
from product.models import *
from order.models import *
from .serializer import *


# Create your views here.
#  HOME PAGE
class HomePage(TemplateView):
    template_name = "restapi/Home.html"

class HomeSec(TemplateView):
    template_name = "restapi/HomeSec.html"

# GET DATA API
class DataGet(ListAPIView):
    queryset = AllOrder.objects.all()
    serializer_class = AllOrderSer

class AllProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductSer

# POST DATA FOR CREATE USER
class Register(APIView):
    def post(self, request, format=None):
        data = request.data
        if CustomUser.objects.filter(phone__exact=data.get('phone')):
            return Response({"stateCode": 201, "msg": "User Exits"}, 201)
        if CustomUser.objects.filter(email__exact=data.get('email')):
            return Response({"stateCode": 202, "msg": "User enn"}, 201)
        new_user = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "password": make_password(data.get("password")),
        }
        # print(new_user)
        serializer = AccountsSeri(data=new_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            username = data.get("phone")
            raw_password = data.get("password")

            cur_user = authenticate(username=username, password=raw_password)

            token, _ = Token.objects.get_or_create(user=cur_user)
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                    "token": token.key,
                },
                200,
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# =============================== LOGIN   =====================================
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("phone")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    # user = authenticate(username=username, password=password)
    try:
        user = authenticate(
            username=CustomUser.objects.get(email__iexact=username), password=password
        )

    except:
        user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid Credentials"}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=HTTP_200_OK)



# ! PRODUCT SEARCH BAR
class SrchProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductSer
    search_fields = ["title", "description"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    
# ---------------------------------------------------------------------------- #
#                                 ! CART METHOD                                 #
# ---------------------------------------------------------------------------- #
class CartPage(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # ! get cart data 
    def get(self, request):
        data = request.data
        usr = str(request.user.id)
        
        
        usrCart = ProductCart.objects.filter(customerCart=usr)

        try:
            ser = CartSer(usrCart, many=True)
            alldata = ser.data

        except:
           
            alldata = ser.errors
        return Response(alldata)
    
    # ! post cart data .get
     # orc PROFILE POST METHOD

    def post(self, request):
        data = request.data
        usr = str(request.user.id) 
        # usr= data.get("customerCart")
        newCart = {
            "quantity": data.get("quantity"),
            "product": data.get("product"),
            "customerCart": str(usr),
            
        }

        if ProductCart.objects.filter(
            Q(customerCart__exact=usr)
            & Q(product__exact=data.get("product"))
        ):
            return Response({"stateCode": 201, "msg": "User Exits"}, 201)
        
        serializer = AddCartSer(data=newCart)
        
      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # orc QUANTITY UPDATE 
    def put(self, request, pk=None):
        data = request.data
        idt = request.data.get("id")
        cus = ProductCart.objects.get(pk=idt)
        
        new_cartu = {
            "quantity": data.get("quantity"),
        }
        serializer = UpCartSer(cus, data=new_cartu)

      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# ! DELETE CART ITEM 
class CartDel(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request,pk=None):
        idt= request.data.get("id") 
        cus = ProductCart.objects.get(pk=idt)
        print(cus)
        if ProductCart.objects.filter(pk=idt).exists():
                card = ProductCart.objects.get(pk=idt)
                
                card.delete()
                res = {"error": False, "msg": "data delete"}
                return Response(res)
        
        else:
            res = {"error": True, "msg": " not have any data"}
        return Response(res)




# ---------------------------------------------------------------------------- #
#                     orc   PROFILE PAGE GET AND POST METHOD                     #
# ---------------------------------------------------------------------------- #
class ProfilePage(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # todo  GET METHOD
    def get(self, request):
        usr = request.user.id
        # usr = str("86fcf28b-13d5-439b-9eca-1852b49783b5")
        prof = Profile.objects.filter(uplod=usr)
        
        try:
            ser = ProfileSer(prof, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)

    # orc PROFILE POST METHOD

    def post(self, request, pk=None):
        data = request.data
        idt = request.data.get("id")
        cus = Profile.objects.get(pk=idt)
        
        new_profile = {
            "fullname": data.get("fullname"),
            "email": data.get("email"),
            "gender": data.get("gender"),
            "pic": data.get("pic"),
        }

        # print(new_profile)
        serializer = ProfileSer(cus, data=new_profile)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------- #
#                   ! ADDRESS POST & GET  METHOD                                     #
# ---------------------------------------------------------------------------- #
class AddressV(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # todo  GET METHOD
    def get(self, request):
        usr = request.user.id
        
        addres = Address.objects.filter(uplod=usr)
        

        try:

            ser = AddressSer(addres, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)

    # orc PROFILE POST METHOD

    def post(self, request, pk=None):
        data = request.data
        usr = str(request.user.id)
        # usr =data.get("uplod")
       

        new_addres = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            "uplod": usr,
        }

        # print(new_addres)
        serializer = PostAddressSer(data=new_addres)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # orc Update Adress
    def put(self, request, pk=None):
        data = request.data
        idt =data.get("id")
        usr=request.user.id
        
        cus = Address.objects.get(pk=idt)
        new_address = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            "uplod": usr
            
        }

        # print(new_profile)
        serializer = PostAddressSer(cus, data=new_address)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        
class AddressDel(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def post(self, request,pk=None):
        idt = request.data.get("id")

        try:
            if Address.objects.filter(pk=idt).exists():
                adr = Address.objects.filter(pk=idt)
              
                adr.delete()
                res = {"error": False, "msg": "data delete"}
            else:
                res = {"error": True, "msg": " not have any data"}

        except:
            res = {"error": True}
        return Response(res)


        



# ---------------------------------------------------------------------------- #
#                                 ! ORDER PAGE                                 #
# ---------------------------------------------------------------------------- #
class OrderPage(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    # !  ORDER REQUEST DATA
    def post(self, request):
        data = request.data
        # usr = str(request.user.id)
        usr=data.get("user")
        adr=data.get("address")
        if Address.objects.filter(Q(uplod=usr) & Q(pk=adr)) :
            new_order = {
               "product": data.get("product"),
                "address": adr,
                "quantity": data.get("quantity"),
                "user": usr,
                }

            serializer = AllOrderSer(data=new_order)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = serializer.save()
                return Response(
                    {
                    "stateCode": 200,
                    "msg": "enter data",
                    }
                )
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response('Address Wrong', status=HTTP_400_BAD_REQUEST)

    # ! CURRENT ORDER data
    def get(self, request):
        usr = request.user
        order = CurrentOrder.objects.filter(user=usr)
        

        try:
            ser = CurrentOrderSer(order, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)


