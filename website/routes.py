from django.contrib import admin
from django.urls import path,include
from website.views import (
    # index,
    Cart,
    Checkout,
    Login,
    Signup,
    checkout_page,
    cart_page,
    home,
    Logout
)

from website.components import (
    OccasionView,
    DetailsView,
    increment_qty as Increase_Qty,
    decrease_qty as Decrease_Qty
)


app_name = 'website'
urlpatterns = [
    path('',home,name="Default"),
    # path('index/', index, name="index"),
    path('login/', Login.as_view(), name="login"),
    path('sign-up/', Signup.as_view(), name="Signup"),
    path('add-to-cart/', Cart.as_view(), name="AddToCart"),
    path('cart/', cart_page, name="cart-page"),
    path('checkout-page/',checkout_page,name="checkout-page"),
    path("checkout/",Checkout.as_view(),name="Checkout"),
    path("logout/",Logout,name="logout"),

    path("Occasion/<slug:occasion_no>",OccasionView.as_view(),name="Occasion-Products"),
    path("Detail/<slug:product_slug>",DetailsView.as_view(),name="Product-Detail"),
    path("increase_qty/",Increase_Qty,name="Increase_Qty"),
    path("decrease_qty/",Decrease_Qty,name="Decrease_Qty")

]
