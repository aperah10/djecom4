from django.urls import path, re_path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls import url

# app_name ='restapi'

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("h/", views.HomeSec.as_view(), name="hsec"),
    path("data/", views.DataGet.as_view(), name="getData"),
    path("p/", views.AllProduct.as_view(), name="product"),
    # ==========POST REQUEST FOR ==================
    # path('login/', obtain_auth_token),
    path("login/", views.login, name="Login"),
    path("reg/", views.Register.as_view(), name="Reg"),
    path("cart/", views.CartPage.as_view(), name="Cart"),
    path('cartdel/',views.CartDel.as_view(), name="cartdel"),
    path("search/", views.SrchProduct.as_view(), name="Searchbar"),
    path("profile/", views.ProfilePage.as_view(), name="Profile"),
    path("address/", views.AddressV.as_view(), name="Address"),
    path("addressdel/", views.AddressDel.as_view(), name="adrdel"),
    path("order/", views.OrderPage.as_view(), name="Order"),
    
 
]
