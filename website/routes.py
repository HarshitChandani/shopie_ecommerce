from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from website.views import (
    # index,
    Cart,
    Checkout,
    Login,
    Signup,
    checkout_page,
    cart_page,
    Home,
    Logout,
    order_summary    
)
from website.components import (
    OccasionView,
    DetailsView,
    ProductCategoryView,
    BrandView,
    increment_qty as Increase_Qty,
    decrease_qty as Decrease_Qty,
    add_address as Add_Address,
    cancel_order as Cancel_Order
)


app_name = 'website'
urlpatterns = [
    path('',Home.as_view(),name="Default"),
    # path('index/', index, name="index"),
    path('login/', Login.as_view(), name="login"),
    path('sign-up/', Signup.as_view(), name="Signup"),
    path('add-to-cart/', Cart.as_view(), name="AddToCart"),
    path('cart/', cart_page, name="cart-page"),
    path('checkout-page/',checkout_page,name="checkout-page"),
    path("checkout/",Checkout.as_view(),name="Checkout"),
    path("logout/",Logout,name="logout"),
    path("orders/",order_summary,name="order-summary"),

    path("Occasion/<slug:occasion_no>",OccasionView.as_view(),name="Occasion-Products"),
    path("Detail/<slug:product_slug>",DetailsView.as_view(),name="Product-Detail"),
    path("Category/<slug:category_no>",ProductCategoryView.as_view(),name="Occasion-Products"),
    path("Brand/<slug:brand_no>",BrandView.as_view(),name="Brand-Products"),
    path("increase_qty/",Increase_Qty,name="Increase_Qty"),
    path("decrease_qty/",Decrease_Qty,name="Decrease_Qty"),
    path("add_address/",Add_Address,name="add_address"),
    path("cancel-order/<slug:order_no>",Cancel_Order,name="cancel-order")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
