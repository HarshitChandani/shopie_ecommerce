from sqlite3 import OperationalError
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
import json
from typing import Any
from website.models import (
   Product as ProductModel,
   Occasion as OccasionModel,
   Brand as BrandModel,
   Pattern as PatternModel,
   ProductCategory as ProductCategoryModel
)
from django.views.generic import (
   View,
   ListView,
   DetailView
)


#OCCASIONS
class OccasionView(ListView):
   context_object_name = "product_data"
   template_name = "index.html"
   
   #override 
   def get_queryset(self):
      product_slug = self.kwargs.get("occasion_no",None)
      return ProductModel.objects.filter(occasion_id__slug=product_slug).only(
         'lg_image','slug','title','fitting_type','selling_price','is_discount_applicable','MRP','discount_percent'
      )


#PRODUCT
class DetailsView(DetailView): 
      """
         This Generic Detail View will get product details according to the product slug. 
      """
      template_name = "detail.html"
      model = ProductModel
      slug_field = "slug"
      slug_url_kwarg = "product_slug"
      context_object_name = "product_data"

      def get_context_data(self, **kwargs: Any):
          context = super().get_context_data(**kwargs)
          context['available_sizes_list'] = self.object.available_size.split(",")
          print(context)
          return context

      # or 
      # ProductModel.objects.filter(slug=product_slug).get()

      # Both above are same But Class based view more readable.


#BRAND
class BrandView(DetailView):
   model = BrandModel
   context_object_name = "brands_data"
   template_name = "home.html"


#CART
def count_cart(request):
   '''
        This method is used to get the count of total items added to the cart.
        @request: request object
        @return: the count i.e; the sum of total items inside cart-items session key.
    '''
   get_count = (
      int(value["user_purchased_qty"])
      for value in request.session["cart_items"].values()
      if not isinstance(value,int)
   )
   return sum(get_count)


#CART


#CART
def count_cart_total(request):
   """Get the total amount of all items which are in the cart. 

   Args:
       request (_type_): _description_

   Returns:
       int: Sum.
   """
   
   cart_total = (
            int(values["user_purchased_qty"]) * values["selling_price"] 
            for values in request.session["cart_items"].values()
            if not isinstance(values,int)
        )
   total = sum(cart_total)
   return total 


def update_qty(request,slug,increment_operation:bool,decrement_operations:bool):
   try:
      previous_purchased_qty = int(request.session["cart_items"][slug]["user_purchased_qty"])
      if increment_operation and not decrement_operations:
         previous_purchased_qty = previous_purchased_qty + 1
      elif not increment_operation and decrement_operations:
         previous_purchased_qty = previous_purchased_qty - 1
      else:
         raise OperationalError("Both increment_operation and decrement_operations cannot be of same value.")
      request.session["cart_items"][slug]["user_purchased_qty"] = str(previous_purchased_qty)
      request.session.modified = True
      print(request.session["cart_items"][slug]["user_purchased_qty"])
   except OperationalError:
      print(OperationalError.__traceback__)


def increment_qty(request):
   """Method to increase the quantity of a particular item by clicking on plus button.

   Args:
       request (_type_): _description_

   Raises:
       KeyError: If the slug of particular item is not in the cart items . That might be a request from a third party.

   Returns:
      HttpResponse : Whether the session is being modified or not. 
   """
   if request.method == "GET":
      slug = request.GET["id"]
      try:
         if slug in request.session["cart_items"]:
            available_qty = request.session["cart_items"][slug]["available_qty"]
            if available_qty != 0:
               update_qty(request,slug,True,False)
               available_qty -= 1
               request.session["cart_items"][slug]["available_qty"]= available_qty
               request.session["cart_items"][slug]["sold_qty"] += 1
               total = count_cart_total(request)
               request.session["cart_items"]["cart_total"] = total
               json_data  = {
                  'cart_updated':True,
                  'cart_total':request.session["cart_items"]["cart_total"],
                  'reason':'Quantity updated'
               }
               request.session.modified = True
            else:
               json_data = {
                  'cart_updated':False,
                  'cart_total':False,
                  'reason':'Not enough quantity is available.'
               }
         else:
            raise KeyError("{} is not in session.".format(slug))
      except KeyError:
         json_data = {
            'cart_updated':False,
            'cart_total':False,
            'reason':'Slug not present.'
         }
   else:
      json_data = {
         'cart_updated':False,
         'cart_total':False,
         'reason':'Invalid Request.'
      }
   return HttpResponse(json.dumps(json_data),content_type="application/json")


def decrease_qty(request):
   """Method to decrease the quantity of a particular item by clicking on plus button.

   Args:
       request (_type_): _description_

   Raises:
       KeyError: If the slug of particular item is not in the cart items . That might be a request from a third party.

   Returns:
       HttpResponse : Whether the session is being modified or not.
   """
   if request.method == "GET":
      slug = request.GET["id"]
      try:
         if slug in request.session["cart_items"]:
            available_qty = request.session["cart_items"][slug]["available_qty"]
            if int(request.session["cart_items"][slug]["user_purchased_qty"]) !=0 :
               update_qty(request,slug,False,True)
               available_qty += 1
               request.session["cart_items"][slug]["available_qty"]= available_qty
               request.session["cart_items"][slug]["sold_qty"] -= 1
               total = count_cart_total(request)
               request.session["cart_items"]["cart_total"] = total
               json_data  = {
                  'cart_updated':True,
                  'cart_total':request.session["cart_items"]["cart_total"],
                  'reason':'Quantity updated'
               }
               request.session.modified = True
            else:
               json_data = {
                  'cart_updated':False,
                  'cart_total':False,
                  'reason':'Not enough quantity is reduce.'
               }
         else:
            raise KeyError("{} is not in session.".format(slug))
      except KeyError:
         json_data = {
            'cart_updated':False,
            'cart_total':False,
            'reason':'Slug not present.'
         }
   else:
      json_data = {
         'cart_updated':False,
         'cart_total':False,
         'reason':'Invalid Request.'
      }
   return HttpResponse(json.dumps(json_data),content_type="application/json")
