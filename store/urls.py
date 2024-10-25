
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('otpverify/',OTPVerificationView.as_view(),name='otpverify'),
     path('users/<int:user_id>/', UserDeleteView.as_view(), name='user-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('sizes/', SizeListView.as_view(), name='size-list'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('baskets/', BasketListView.as_view(), name='basket-list'),
    path('basket-items/', BasketItemListView.as_view(), name='basket-item-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
]
