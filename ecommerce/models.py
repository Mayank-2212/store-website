from django.db import models
from accounts.models import Account
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique = True , null = True , blank = True)
    image = models.ImageField(upload_to = "categories")
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category , self).save(*args , *kwargs)

    def __str__(self):
        return self.category_name
    


class ColorVariant(models.Model):
    color = models.CharField(max_length=40)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.color

class SizeVariant(models.Model):
    size_name = models.CharField(max_length=40)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.size_name
    
class Products(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique = True , null = True , blank = True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name = "products" , null=True , blank=True)
    price = models.IntegerField()
    description = models.TextField(max_length=1000)
    product_image = models.ImageField(upload_to = "products_images" , null=True , blank=True)
    color_variants = models.ManyToManyField(ColorVariant , blank=True)
    size_variants = models.ManyToManyField(SizeVariant ,  blank=True)

    def __str__(self):
        return f"{self.product_name} {self.price}"
    
    def get_product_price_by_size(self,size):
        return self.price + SizeVariant.objects.get(size_name=size).price

class ProductImage(models.Model):
    product = models.ForeignKey(Products , on_delete=models.CASCADE , related_name = "product_images" )
    product_image = models.ImageField(upload_to ="products_images")



class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = 'carts')
    is_paid = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.user}"

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'cart_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE )
    quantity = models.IntegerField(default = 1)
    color_variant = models.ForeignKey(ColorVariant , on_delete=models.SET_NULL , null=True , blank=True)
    size_variant = models.ForeignKey(SizeVariant , on_delete=models.SET_NULL , null=True , blank=True)
    total_price = models.IntegerField(default = 0 , null=True , blank=True)
    
    def sub_total(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.product} {self.quantity} {self.color_variant} {self.size_variant}"