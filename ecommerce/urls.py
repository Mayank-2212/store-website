from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('remove/<int:id>/',views.remove, name='remove'),
    path('details/<slug:product_slug>/',views.details, name='details'),
    path('add_to_cart/<slug:product_slug>/',views.cart,name='add_to_cart'),
    path('cart_details/',views.cart_details, name='cart_details'),
    path("plus/<int:id>",views.plus,name='plus'),
    path("minus/<int:id>",views.minus,name='minus'),
    path('store/',views.store,name='store'),
    path('checkout/',views.checkout,name='checkout'),
    path('place_order/',views.place_order,name='place_order')
]
