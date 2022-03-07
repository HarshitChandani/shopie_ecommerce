from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
import json
# import Exception
from datetime import datetime

from .models import (
    Product as ProductModel,
    Occasion as OccasionModel ,
    Product_OrderDetails as Product_OrderDetailsModel,
    Orders as OrdersModel,
    Brand as BrandModel,
    ProductCategory as ProductCategoryModel,
    Shipping_Address as ShippingAddressModel
)
from .components import (
    count_cart,
    count_cart_total,
    update_qty
)
from django.shortcuts import (
    render, 
    redirect, 
    HttpResponse,
    get_object_or_404
)
from django.views.generic import (
   View,
   ListView,
   DetailView
)

# DEFAULT
class Home(ListView):
    context_object_name = "brand_data"
    template_name = 'home.html'
    model = BrandModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_data"] =  ProductCategoryModel.objects.all().order_by('pk')[:3]
        return context
    

# CART
def cart_page(request):
    return render(request, "cart.html")

# LOGIN / SIGNUP
class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("website:Default")
        return render(request,"login.html")

    def post(self, request, *args, **kwargs):
        try:
            loginUsername, loginPassword = request.POST['username'], request.POST['password']
            validate_email(loginUsername)
        except ValidationError:
            messages.error(request,"Email Format is not correct.")
        else:
            user = authenticate(username=loginUsername, password=loginPassword)
            if user is not None:
                login(request, user)
                if request.POST["next"] != "":
                    return redirect(request.POST["next"])
                else:
                    return redirect('website:Default')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect("website:login")
        
# LOGIN / SIGNUP
class Signup(View):
    def get(self, request, *args, **kwargs):
        return render(request,"signup.html")

    def post(self, request, *args, **kwargs):
        try:
            f_name,l_name,username,email,password = request.POST.get('first_name'),request.POST.get('last_name'),request.POST.get('username'),request.POST.get('username'),request.POST.get('password')
            validate_email(email)
        except ValidationError:
            messages.error(request,"Email Format is not correct.")
        else:
            if (User.objects.filter(username=username).exists()):
                messages.error(request,"User already exists.")
                return redirect("website:Signup")
            else:
                new_user = User.objects.create(
                    first_name=f_name.capitalize(), 
                    last_name=l_name.lower(),
                    username=username, 
                    email=email, 
                    password=password,
                    is_active=True, 
                    is_staff=False
                )
                new_user.save()
                messages.success(request,"Hello, {} {}. Kindly login.".format(f_name.capitalize(),l_name.lower()))
                return redirect('website:login')

# LOGIN / SIGNUP
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("website:Default")

#CART
class Cart(View):

    def get(self,request):
        # count cart items 
        return HttpResponse(count_cart(request))
        
        
    def post(self, request):
        slug = request.POST["product_slug"]
        user_selected_product_size = request.POST["user_selected_size"]
        default_quantity = int(request.POST["default_qty"])
        
        data = ProductModel.objects.filter(slug=slug).get()
        request.session["modified"]=False
        if "cart_items" not in request.session:
            request.session["cart_items"] = {}
        
        if slug not in request.session["cart_items"]:
            request.session["cart_items"][slug] = {
                "product_slug":slug,
                "user_purchased_qty":default_quantity,
                "user_selected_product_size":user_selected_product_size,
                "title":data.title,
                "sold_qty":( data.sold_qty + default_quantity ),
                "available_qty":(data.available_qty - default_quantity),
                "selling_price":data.selling_price,
                "MRP":data.MRP,
                'image':data.sm_image,
                "is_discount_applicable":data.is_discount_applicable,
                "discount_percent":data.discount_percent,
                "brand":data.brand_id.title,
                "occasion":data.occasion_id.title,
            }
            request.session["modified"]=True
        else:
            available_qty_in_cart = request.session["cart_items"][slug]["available_qty"]
            sold_qty_in_cart = request.session["cart_items"][slug]["sold_qty"] 
            if request.session["cart_items"][slug]["available_qty"] != 0:
                request.session["cart_items"][slug]["available_qty"] = available_qty_in_cart - 1  
                request.session["cart_items"][slug]["sold_qty"] = sold_qty_in_cart +1
                if (update_qty(request,slug,True,False)):
                    request.session["modified"]=True
            else:
                request.session["modified"]=False        

        request.session["cart_items"]["cart_total"] = count_cart_total(request)
        request.session.modified = True
        return HttpResponse(request.session["modified"])
    

# CHECKOUT
@login_required
def checkout_page(request):
    if request.user.is_authenticated and "cart_items" in request.session:
        print("User is Logged in and also has items in cart.")
        shipping_address_obj = ShippingAddressModel.objects.filter(user_id=request.user.id).all()
        context = {
            'data':shipping_address_obj,
            'cart_total':request.session["cart_items"]["cart_total"]
        }
        return render(request,"checkout.html",context)
    else:
        return redirect('website:Default')

# CHECKOUT
class Checkout(LoginRequiredMixin,View):
    def post(self, request):
        if "cart_items" in request.session and request.user.is_authenticated:
            address_id = request.POST["address_id"]
            print("User has added some items.")
            order_key = "{}_{}".format("order",OrdersModel.objects.count()+1)  
            ordered_items_list = list()
            for item in request.session["cart_items"].values():
                if not isinstance(item,int):
                    # item exists.
                    discount_amt = (item["MRP"] * item["discount_percent"]) // 100 if item["is_discount_applicable"] else 0
            
                    ordered_items_list.append(
                        Product_OrderDetailsModel(
                            order_key = order_key,
                            product_id = get_object_or_404(ProductModel,slug=item["product_slug"]),
                            ordered_size = item["user_selected_product_size"],
                            ordered_color = None,
                            ordered_product_image = item["image"],
                            ordered_qty= int(item["user_purchased_qty"]),
                            SP = item["selling_price"],
                            MRP = item["MRP"],
                            discount= discount_amt, 
                            total = item["selling_price"] * int(item["user_purchased_qty"])
                        )
                    )
                    
                    # Update Product Model
                    ProductModel.objects.filter(slug=item["product_slug"]).update(
                        sold_qty = item["sold_qty"],
                        available_qty = item["available_qty"],
                        is_out_of_stock = False if item["available_qty"] != 0 else True
                    )
            # Product Model has been created according to the new values.
            Product_OrderDetailsModel.objects.bulk_create(ordered_items_list)
                    
                # Create new record in Order Model                   
            orders_detail_obj = Product_OrderDetailsModel.objects.filter(
                order_key=order_key
            ).all()

            order_total = (t.total for t in orders_detail_obj)
            # print(*order_total)
            order_amt = sum(order_total)
            print("Order Amount: {}".format(order_amt))
        
            user_shipping_address = get_object_or_404(
                ShippingAddressModel,
                user_id=request.user.id,
                pk=address_id
            )

            ShippingAddressModel.objects.filter(
                pk=address_id
            ).update(
                is_active = True
            )

            place_order = OrdersModel(
                order_date = datetime.now().date(),
                shipping_address = user_shipping_address,
                gross_amt = order_amt, 
                user = request.user,
                order_key = order_key,
                shipping = 0
            )
            place_order.save()
            
            print("Order placed.")
            print("Order Number: {order_no}".format(order_no=place_order.id))
            del request.session["cart_items"]
            return HttpResponse(
                json.dumps({
                    'order_placed':True,
                    # 'order_id':place_order.id,
                    'redirect':True
                }),content_type="application/json"
            )
        else:
            return HttpResponse(json.dumps(
                {
                    'order_placed':False,
                }
            ))

@login_required
def order_summary(request):
    try:
        orders = OrdersModel.objects.filter(
            user = request.user
        ).all()
        context = {
            'orders':orders
        }
        print(orders)
        return render(request,"order-summary.html",context)
    except ObjectDoesNotExist:
        print("No order has been placed yet.")
    