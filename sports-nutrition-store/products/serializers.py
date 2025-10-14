from rest_framework import serializers
from .models import Brand, Category, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'brand_name', 'category', 'category_name',
                  'description', 'price', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']