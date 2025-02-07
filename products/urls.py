from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CreateOrderView, VerifyPaymentView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create-order/', CreateOrderView.as_view()),
    path('verify-payment/', VerifyPaymentView.as_view()),
]
