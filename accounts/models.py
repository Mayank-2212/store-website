from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from ecommerce.models import *
# Create your models here.
#here we are customizing admin model
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,password=None):
        if not email:
            raise ValueError("User must have an email address")

        

        user=self.model(
            email=self.normalize_email(email),
            
            first_name=first_name,
            last_name=last_name,
        )
        user.is_user = True
        user.set_password(password)#set_passwrd()is use to set password in encrypted manner
        user.is_active = True
        user.save(using=self._db)
        return user
    

    def create_superuser(self,first_name,last_name,email,password):

        user=self.model(    
            email=self.normalize_email(email), 
            password=password,
            first_name=first_name,
            last_name=last_name,

        )
        user.is_admin=True
        user.is_staff=True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    


class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=20)
    country = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    street = models.CharField(max_length=100,null=True,blank=True)
    building = models.CharField(max_length=50,null=True,blank=True)
    house = models.CharField(max_length=50,null=True,blank=True)
    postal_code = models.IntegerField(null=True,blank=True)
    zip =  models.CharField(max_length=50,null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_user=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']
    def has_perm(self,perm,obj=None):
        return self.is_admin

    objects=MyAccountManager()

    def has_module_perms(self,add_label):
        return True
    
    def __str__(self):
        return self.email   
    

    @property
    def get_cart_count(self):
        from ecommerce.models import CartItems,Cart
        item_count = CartItems.objects.filter(cart__user=self.id,cart__is_paid=False).count()
        return item_count