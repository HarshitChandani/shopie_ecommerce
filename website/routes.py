from django.contrib import admin
from django.urls import path,include
from website.views import (
    # index,
    home,
    loginForm,
    signupForm,
    handleLogin,
    handleSignup,
    Cart,
    checkout_page,
    cart_page,
    Checkout
)

from website.components import (
    OccasionView,
    DetailsView,
    increment_qty as Increase_Qty,
    decrease_qty as Decrease_Qty
)


urlpatterns = [
    path('',home,name="Default"),
    # path('index/', index, name="index"),
    path('login/', loginForm, name="loginForm"),
    path('sign-up/', signupForm, name="signupForm"),
    path('handle-login/', handleLogin, name="handleLogin"),
    path("handle-sign-up/", handleSignup, name="handleSignup"),
    path('add-to-cart/', Cart.as_view(), name="AddToCart"),
    path('cart/', cart_page, name="cart-page"),
    path('checkout-page/',checkout_page,name="checkout-page"),
    path("checkout/",Checkout.as_view(),name="Checkout"),
    
    path("Occasion/<slug:occasion_no>",OccasionView.as_view(),name="Occasion-Products"),
    path("Detail/<slug:product_slug>",DetailsView.as_view(),name="Product-Detail"),
    path("increase_qty/",Increase_Qty,name="Increase_Qty"),
    path("decrease_qty/",Decrease_Qty,name="Decrease_Qty")

]
