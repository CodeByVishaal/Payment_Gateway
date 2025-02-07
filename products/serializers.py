from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only =True)
    name = serializers.CharField(min_length=4, required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    product_image = serializers.ImageField(required=False)
    description = serializers.CharField(style={'base_template': 'textarea.html'}, max_length=700, required=False)

    class Meta:
        model = Products
        fields = ['id','name', 'price', 'description', 'product_image']  # Include all model fields in the API

class ProductUpdateSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only =True)
    name = serializers.CharField(min_length = 4, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    product_image = serializers.ImageField(required=False)
    description = serializers.CharField(style={'base_template': 'textarea.html'}, max_length=700, required=False)

    class Meta:
        model = Products
        fields = ['id','name', 'price', 'description', 'product_image']  # Include all model fields in the API

    def update(self, instance, validated_data):
        validated_data.pop('id', None)

        for attr, data in validated_data.items():
            setattr(instance, attr, data)

        instance.save()
        print(instance)

        return instance