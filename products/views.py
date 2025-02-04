from rest_framework import generics
from .models import Products
from .serializers import ProductSerializer

# Create API Views using Django REST Framework (DRF)

# GET all products (List) and POST new product (Create)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all().order_by('created_at')
    serializer_class = ProductSerializer

# GET a single product (Retrieve), UPDATE, DELETE
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all().order_by('created_at')
    serializer_class = ProductSerializer
