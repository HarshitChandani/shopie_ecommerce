from atexit import register
from django.contrib import admin
from django.contrib.sessions.models import Session
from website.models import (
   Occasion,
   Product,
   ProductCategory,
   Brand,
   Pattern,
   Orders,
   Shipping_Address,
   Product_OrderDetails
   )


class ProductAdmin(admin.ModelAdmin):
   fields = (
      'title',
      'MRP',
      'selling_price',
      'descriptions',
      'lg_image',
      'sm_image',
      'is_out_of_stock',
      'available_qty',
      'sold_qty',
      'purchase_qty',
      'colors_availables',
      'fabric',
      'sleeve_type',
      'fitting_type',
      'available_size',
      'is_discount_applicable',
      'occasion_id',
      'category_id',
      'pattern_id',
      'brand_id'
   )
   exclude = (
      'slug',
      'discount_percent'
   )

   list_display = [
      'pk',
      'slug',
      'title',
      'MRP',
      'selling_price',
      'purchase_qty',
      'sold_qty',
      'available_qty',
      'discount_percent',
   ]


class BrandAdmin(admin.ModelAdmin):
   
   list_display = [
      'pk',
      'slug',
      'title'
   ]


class OrdersAdmin(admin.ModelAdmin):
   list_display = [
      'pk',
      'slug',
      'order_date',
      'order_confirm',
      'order_received',
      'gross_amt',
      'shipping',
      'net_amt',
      'get_items'
   ]
   exclude = [
      'slug',
      'net_amt'
   ]
   
class Product_OrderDetailsAdmin(admin.ModelAdmin):
   fields = [
      'product_id',
      'order_key',
      'ordered_size',
      'ordered_color',
      'ordered_product_image',
      'ordered_qty',
      'SP',
   ]
   list_display = [
      'product_id',
      'order_key',
      'ordered_size',
      'ordered_color',
      'ordered_product_image',
      'MRP',
      'discount',
      'SP',
      'ordered_qty',
      'total',
   ]


class SessionAdmin(admin.ModelAdmin):
   def _session_data(self,obj):
      return obj.get_decoded()

   list_display = [
      'session_key',
      '_session_data',
      'expire_date'
   ]

class ShippingAddressAdmin(admin.ModelAdmin):
   list_display = [
      'pk',
      'address',
      'state',
      'country',
      'pincode',
      'user_id',
      'is_active'
   ]  
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Pattern)
admin.site.register(Occasion)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(Shipping_Address,ShippingAddressAdmin)
admin.site.register(Product_OrderDetails,Product_OrderDetailsAdmin)
admin.site.register(Session,SessionAdmin)