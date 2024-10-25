from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string
from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):

    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateField(auto_now_add=True)

    updated_date=models.DateField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):
        return  self.name

class Size(models.Model):

    name = models.CharField(max_length=100, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):

        return self.name 


class Brand(models.Model):

    name = models.CharField(max_length=100, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        
        return self.name


    

class Product(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(null=True, blank=True)

    size_object = models.ManyToManyField(Size)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='product_images',null=True, blank=True, default='product_images/default.jpg')

    price = models.PositiveIntegerField()

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.title
    


class Basket(models.Model):

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.owner.username

class BasketItem(models.Model):

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='cartitems')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    is_order_placed=models.BooleanField(default=False)



class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='myorders')

    basket_item = models.ManyToManyField(BasketItem)

    delivery_address = models.CharField(max_length=250)

    phone = models.CharField(max_length=12)

    email = models.CharField(max_length=100)

    pay_options = (
        ('online', 'online'),
        ('cod', 'cod')
    )

    payment_mode = models.CharField(max_length=100, choices=pay_options, default='cod')

    order_id = models.CharField(max_length=200, null=True)

    is_paid = models.BooleanField(default=False)

    order_status = (
        ('order_confirmed', 'Order confirmed'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),

    )

    status = models.CharField(max_length=200, choices=order_status, default='order_confirmed')

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)





# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     objects = CustomUserManager()
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']


from django.contrib.sessions.models import Session
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user( email, password, **extra_fields)
    

# class CustomUser(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     current_token = models.CharField(max_length=255, null=True, blank=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name','last_name']

#     def _str_(self):
#         return self.email


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=150, unique=False,)
    last_name=models.CharField(max_length=150,unique=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

# class OTPCode(models.Model):
#     user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     email = models.EmailField()
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_verified = models.BooleanField(default=False)

class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


    # def generate_otp(self):
    #     self.otp = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    #     self.save()

    # def is_expired(self):
    #     expiration_time = timezone.now() - timezone.timedelta(minutes=10)  
    #     return self.created_at < expiration_time

    # def __str__(self):
    #     return f'{self.email} - {self.otp}'
    def is_valid(self):
        """Check if the OTP is still valid (e.g., within a 5-minute window)."""
        return (timezone.now() - self.created_at).total_seconds() < 300

    



class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    