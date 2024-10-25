from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Category, Size, Brand, Product, Basket, BasketItem, Order, CustomUser,OTP
from .serializers import CategorySerializer, SizeSerializer, BrandSerializer, ProductSerializer, BasketSerializer, BasketItemSerializer, OrderSerializer
from .permissions import IsAdminUserOrReadOnly
from store.models import CustomUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from .serializers import OTPVerificationSerializer
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterSerializer, OTPVerificationSerializer, LoginSerializer
import pyotp

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                otp = pyotp.TOTP(pyotp.random_base32())
                otp_code = otp.now()
                OTP.objects.update_or_create(user=user, defaults={'otp': otp_code})
                try:
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp_code}',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    response_data = {
                        "status": 1,  
                        "message": "User created. Please verify your OTP."
                    }
                except BadHeaderError:
                    return Response({"error": "Invalid header found."}, status=status.HTTP_400_BAD_REQUEST)
              
                return Response({"message": "User created. Please verify your OTP."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OTPVerificationView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
        try:
            serializer = OTPVerificationSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = request.user
                otp_record = OTP.objects.get(user=user)
                otp_record.delete() 
                response_data = {
                            "status": 1,
                            "message": "OTP verified successfully."
                        } 
                return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             response_data = {
                "status": 0,
                "error": "An unexpected error occurred: " + str(e)
            }
             return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(): 
                user = serializer.validated_data
                auth_login(request, user)
                return Response({"message": "Logged in successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserDeleteView(APIView):
    def delete(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)





# class UserRegistrationView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)

#         email = request.data.get('email')
#         try:
#             user = CustomUser.objects.get(email=email)
#             if serializer.is_valid():
#                 user = serializer.save()
#             send_otp_email(user)
#             return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


   
# class verifyotpView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def post(self,request):
#         serializer = OTPVerificationSerializer(data=request.data)
#         if serializer.is_valid():
#             otp_code = OTPCode.objects.get(email=serializer.validated_data['email'], otp=serializer.validated_data['otp'], is_verified=False)
#             if otp_code.is_expired():
#                 return Response({'error': 'OTP code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
#             otp_code.is_verified = True
#             otp_code.save()
#             return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLoginView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         user = CustomUser.objects.filter(email='hafnaali6@gmail.com').first()
#         print(user)
#         return Response({'error': 'Invalid credentials'}, status=400)
    

class CategoryListView(APIView):
    permission_classes=[[permissions.IsAuthenticated]]

    def get(self,request):
        try:
            categories=Category.objects.all()
            serializer=CategorySerializer(categories,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred while retrieving categories: {e}")
            return Response({"error": "An unexpected error occurred while retrieving categories."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def post(self,request):
        try:
            serializer=CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
        except Exception as e:
            print(f"An error occurred while retrieving categories: {e}")
            return Response({"error": "An unexpected error occurred while retrieving categories."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class SizeListView(APIView):
    permission_classes=[[permissions.IsAuthenticated]]
    def get(self,request):
        try:
            sizes=Size.objects.all()
            serializer=SizeSerializer(sizes,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred while retrieving sizes: {e}")
            return Response({"error": "An unexpected error occurred while retrieving sizes."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        try:
            serializer=SizeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
        except Exception as e:
            print(f"An error occurred while retrieving sizes: {e}")
            return Response({"error": "An unexpected error occurred while retrieving sizes."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class BrandListView(APIView):
    permission_classes=[[permissions.IsAuthenticated]]
    def get(self,request):
        try:
            brands=Brand.objects.all()
            serializer=BrandSerializer(brands,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred while retrieving brands: {e}")
            return Response({"error": "An unexpected error occurred while retrieving brands."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self,request):
        try:
            serializer=BrandSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
        except Exception as e:
            print(f"An error occurred while retrieving brands: {e}")
            return Response({"error": "An unexpected error occurred while retrieving brands."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProductListView(APIView):
    permission_classes=[[permissions.IsAuthenticated]]

    def get(self,request):
        try:
            products=Product.objects.all()
            serializer=ProductSerializer(products,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred while retrieving products: {e}")
            return Response({"error": "An unexpected error occurred while retrieving products."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    
    def post(self,request):
        try:
            serializer=ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
        except Exception as e:
            print(f"An error occurred while retrieving products: {e}")
            return Response({"error": "An unexpected error occurred while retrieving products."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

   

class BasketListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            baskets = Basket.objects.all()
            serializer = BasketSerializer(baskets, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred while retrieving baskets: {e}")
            return Response({"error": "An unexpected error occurred while retrieving baskets."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self, request):
        try:
            serializer = BasketSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print(f"An error occurred while retrieving baskets: {e}")
            return Response({"error": "An unexpected error occurred while retrieving baskets."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BasketItemListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            basket_items = BasketItem.objects.all()
            serializer = BasketItemSerializer(basket_items, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred while retrieving basketitems: {e}")
            return Response({"error": "An unexpected error occurred while retrieving basketitems."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = BasketItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print(f"An error occurred while retrieving basketitems: {e}")
            return Response({"error": "An unexpected error occurred while retrieving basketitems."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred while retrieving orders: {e}")
            return Response({"error": "An unexpected error occurred while retrieving orders."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        
            return Response(serializer.errors,status=400)
        except Exception as e:
            print(f"An error occurred while retrieving orders: {e}")
            return Response({"error": "An unexpected error occurred while retrieving orders."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        






# class UserRegistrationView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [permissions.AllowAny]

# class CategoryListView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminUserOrReadOnly]

# class SizeListView(generics.ListCreateAPIView):
#     queryset = Size.objects.all()
#     serializer_class = SizeSerializer
#     permission_classes = [IsAdminUserOrReadOnly]

# class BrandListView(generics.ListCreateAPIView):
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer
#     permission_classes = [IsAdminUserOrReadOnly]

# class ProductListView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAdminUserOrReadOnly]

# class BasketListView(generics.ListCreateAPIView):
#     queryset = Basket.objects.all()
#     serializer_class = BasketSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class BasketItemListView(generics.ListCreateAPIView):
#     queryset = BasketItem.objects.all()
#     serializer_class = BasketItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class OrderListView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]



