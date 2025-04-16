from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Category)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage 

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":('product_name',)}
    list_display = ['product_name' , 'price']
    inlines = [ProductImageAdmin]
    
@admin.register(ColorVariant)
class ColorVariant(admin.ModelAdmin):
    list_display = ['color' , 'price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariant(admin.ModelAdmin):
    list_display = ['size_name' , 'price']
    model = SizeVariant

admin.site.register(Products, ProductAdmin)

admin.site.register(ProductImage)

admin.site.register(Cart)
admin.site.register(CartItems)