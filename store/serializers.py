from rest_framework import serializers
from .models import Category, Size, Brand, Product, Basket, BasketItem, Order, CustomUser,OTP
# from django_otp.plugins.otp_email.models import EmailDevice

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name','last_name','email', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'first_name': {'required': False},
#             'last_name': {'required': False}
#         }

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         EmailDevice.objects.create(user=user, email=user.email)
#         return user
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import OTP
import pyotp

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model =CustomUser
        fields = ['first_name','last_name', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        otp_code = data.get('otp')
        user = self.context['request'].user

        try:
            otp_record = OTP.objects.get(user=user)
            otp = pyotp.TOTP(otp_record.otp)
            if not otp.verify(otp_code):
                raise serializers.ValidationError("Invalid OTP")
        except OTP.DoesNotExist:
            raise serializers.ValidationError("OTP does not exist")

        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


# class OTPVerificationSerializer(serializers.Serializer):
#     otp = serializers.CharField()
#     email = serializers.EmailField()

#     def validate(self, data):
#         try:
#             otp_code = EmailDevice.objects.get(email=data['email'], otp=data['otp'], is_verified=False)
#         except EmailDevice.DoesNotExist:
#             raise serializers.ValidationError("Invalid OTP or email.")
        
#         if otp_code.is_expired():
#             raise serializers.ValidationError("OTP code has expired.")

#         return data

# class OTPVerificationSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)

#     def validate(self, data):
#         email = data.get('email')
#         otp = data.get('otp')
        
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             raise serializers.ValidationError("User does not exist.")
        
#         try:
#             otp_code = OTPCode.objects.get(user=user, otp=otp)
#         except OTPCode.DoesNotExist:
#             raise serializers.ValidationError("Invalid OTP.")
        
#         if not otp_code.is_valid():
#             raise serializers.ValidationError("OTP has expired.")
        
#         return data

#     def save(self):
#         email = self.validated_data['email']
#         user = CustomUser.objects.get(email=email)
#         user.is_active = True
#         user.save()
from rest_framework import serializers
from store.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email','first_name','last_name','password']  # Add fields you need


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    size_object = SizeSerializer(many=True)
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = '__all__'

class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    size = SizeSerializer()

    class Meta:
        model = BasketItem
        fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
    cartitems = BasketItemSerializer(many=True)

    class Meta:
        model = Basket
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    basket_item = BasketItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
