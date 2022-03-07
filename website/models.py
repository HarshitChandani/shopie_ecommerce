from django.db import models
from django.utils.text import slugify
from django.core.validators import validate_comma_separated_integer_list
from datetime import datetime
import uuid
import os
from django.conf import settings

fabrics = [
    ('Cotton', "Cotton"),
    ('Teri-cotton', "Teri-Cotton"),
    ('Lycra', "Lycra"),
    ('Polyster', "Polyster"),
    ('Silk', "Silk"),
    ('Denim', "Denim")
]

sleeve_type = [
    ('Full-sleeve', "Full Sleeve"),
    ('Half-sleeve', "Half Sleeve"),
    ('3/4-sleeve', "3/4 Sleeve"),
    ('None',"None")
]
fitting_type = [
    ('Slim', "Slim"),
    ('Comform', "Comfort"),
    ('Loose', "Loose"),
    ('Bomber', "Bomber"),
    ('None',None)
]

pattern_type = [
    ('Printed', "Printed"),
    ('Plain', "Plain"),
    ('Checks', "Checks"),
    ("Floral", "Floral"),
    ('Ripped',"Ripped")
]

categorys = [
    ('Jeans', "Jeans"),
    ('Trousers', "Trousers"),
    ('Pants', "Pants"),
    ('Joggers', "Joggers"),
    ('Jogger_cargo', "JoggerCargo"),
    ("Cargo", "Cargo"),
    ("Lycra_pants", "Lycra Pants"),
    ('t-shirts',"T-Shirts"),
    ('shirts','Shirts'),
]


def path_and_rename(instance,filename):
    upload_path = ''
    '''
        Ex: Filename: hello.png
        filename.split('.')[-1] => ['hello','png']
    '''
    extension = filename.split(".")[-1]
    obj = datetime.now() 
    filename = "{}-{}-{}-{}:{}:{}.{}".format(obj.year,obj.month,obj.day,obj.hour,obj.minute,obj.second,extension)
    return os.path.join(upload_path,filename)


# Product Category Model
class ProductCategory(models.Model):
    slug = models.CharField(max_length=255,default="a")
    title = models.CharField("Title", choices=categorys, max_length=100)
    image = models.ImageField(upload_to=path_and_rename,max_length=254)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.slug = slugify("{} {}".format(self.title,"category"))
        super(ProductCategory, self).save(*args, **kwargs)

#Occasion Model
class Occasion(models.Model):
    slug = models.SlugField(default="a",unique=True)
    title = models.CharField("Occasion Title",max_length=100,unique=True)
    image = models.FileField(upload_to=path_and_rename,max_length=254,null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.slug = slugify("{} {}".format(self.title.lower(),"occasion") )
        super(Occasion,self).save(*args, **kwargs)
    

# Brand Model
class Brand(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100,default="a",unique=True)
    label = models.TextField()
    image = models.ImageField(upload_to=path_and_rename,max_length=254,null=True)
    total_products = models.IntegerField(default=0)
    products_type = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug =slugify("{} {}".format(self.title,"brand"))
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# Pattern Models
class Pattern(models.Model):
    slug = models.CharField(max_length=100,unique=True,default="a")
    title = models.CharField(max_length=100,choices=pattern_type, null=True,unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify("{} {}".format(self.title.upper(),"pattern"))
        super(Pattern, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# Product Model
class Product(models.Model):
    slug = models.SlugField(unique=True,default="a")
    title = models.CharField(max_length=100)
    selling_price = models.IntegerField(null=False,default=0,help_text="Selling Price must be greater than MRP.")
    MRP = models.IntegerField(null=False, default=0,help_text="MRP must be smaller than or equal to Selling price.")
    descriptions = models.TextField(null=True)
    lg_image = models.TextField()
    sm_image = models.TextField()
    more_images = models.TextField()
    is_out_of_stock = models.BooleanField(default=False)
    available_qty = models.IntegerField(null=False)
    sold_qty = models.IntegerField(null=False)
    purchase_qty = models.IntegerField(null=False)
    colors_availables = models.TextField(blank=True)
    fabric = models.CharField("Fabric", choices=fabrics, max_length=100)
    sleeve_type = models.CharField("Sleeve Length", choices=sleeve_type, max_length=100)
    fitting_type = models.CharField("Fitting Type", choices=fitting_type, max_length=100)
    available_size = models.CharField(max_length=200,validators=[validate_comma_separated_integer_list],help_text="Enter size seperated with commans.",default=32)
    is_discount_applicable = models.BooleanField(default=False,help_text="Check If this product is in discount scheme and discount percent will be auto calculated.")
    discount_percent = models.IntegerField(null=False,default=0)
    occasion_id = models.ForeignKey(Occasion,on_delete=models.CASCADE)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)
    pattern_id = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.slug = generateSlug()
        self.title = self.title.capitalize()
        if self.is_discount_applicable:
            self.get_discount_percent()
            super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_discount_percent(self):
        difference_amt = self.MRP - self.selling_price
        discount_percent = (difference_amt * 100)//self.MRP
        self.discount_percent = discount_percent


class Shipping_Address(models.Model):
    address = models.TextField()
    landmark = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=100,null=True)
    pincode = models.BigIntegerField()
    country = models.CharField(max_length=100,default="India",null=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_active = models.BooleanField(help_text="Your Active Address",default=True)


class Product_OrderDetails(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    order_key = models.CharField(max_length = 255)
    ordered_size = models.IntegerField(null=False,default=32)
    ordered_color = models.CharField(max_length=255,null=True)
    ordered_product_image = models.TextField()
    ordered_qty = models.IntegerField(default=0)
    MRP = models.IntegerField(null=False, default=0)
    SP = models.IntegerField("S.P(Selling Price)",null=False,default=0)
    discount = models.IntegerField("Discount",null=False,default=0)
    total = models.IntegerField("Total (SP * Qty)",null=False,default=0)
        
    class Meta:
        verbose_name_plural = "Product_OrderDetails"

    # order_key : is a key which is used to track that the these different items belong to same order.


class Orders(models.Model):
    """
        Calculation:
            Gross Amount: Total of all items (item price - discount)
            Net Amount: Gross Amount + Shipping 
    """
    #fields: 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    slug = models.SlugField(unique=True,default="a")
    order_date = models.DateField(null=True)
    order_confirm = models.BooleanField(default=True)
    order_received = models.BooleanField(default=False)
    order_cancelled = models.BooleanField(default=False)
    # one order can have multiple items
    order_key = models.CharField(max_length=255,null=True)
    shipping_address = models.ForeignKey(Shipping_Address,on_delete=models.SET_NULL,null=True)
    gross_amt = models.FloatField("Gross Order Total",null=False,default=0.0)
    shipping = models.IntegerField("Shipping Charges",default=0,null=False)
    net_amt = models.FloatField("Net Order Total",null=False)
    
    def save(self, *args, **kwargs):
        self.slug = generateSlug()
        self.net_amt = self.get_net_order_total()
        super(Orders, self).save(*args, **kwargs)

    def get_net_order_total(self):
        return (self.gross_amt + self.shipping)
    
    
    class Meta:
        verbose_name_plural = 'Orders'

def generateSlug() -> models.SlugField:
        return slugify("{} {}".format(int(datetime.now().timestamp()),uuid.uuid4()))


