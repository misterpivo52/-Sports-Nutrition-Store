import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer

logger = logging.getLogger(__name__)


class BrandListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        logger.info(f"Brand list accessed by user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        logger.info(f"Brand creation attempt by user: {request.user.username}")
        if not request.user.is_staff:
            logger.warning(f"Non-staff user {request.user.username} attempted to create brand")
            return Response(
                {'error': 'Only staff users can create brands'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Brand {serializer.data['name']} created by {request.user.username}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        logger.info(f"Brand detail accessed for pk {pk} by user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    def put(self, request, pk):
        logger.info(f"Brand update attempt for pk {pk} by user: {request.user.username}")
        if not request.user.is_staff:
            logger.warning(f"Non-staff user {request.user.username} attempted to update brand {pk}")
            return Response(
                {'error': 'Only staff users can update brands'},
                status=status.HTTP_403_FORBIDDEN
            )
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Brand {pk} updated by {request.user.username}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        logger.info(f"Brand deletion attempt for pk {pk} by user: {request.user.username}")
        if not request.user.is_staff:
            logger.warning(f"Non-staff user {request.user.username} attempted to delete brand {pk}")
            return Response(
                {'error': 'Only staff users can delete brands'},
                status=status.HTTP_403_FORBIDDEN
            )
        brand = get_object_or_404(Brand, pk=pk)
        if brand.products.exists():
            return Response(
                {'error': 'Cannot delete brand with associated products'},
                status=status.HTTP_400_BAD_REQUEST
            )
        brand.delete()
        logger.info(f"Brand {pk} deleted by {request.user.username}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        logger.info(f"Category list accessed by user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        logger.info(f"Category creation attempt by user: {request.user.username}")
        if not request.user.is_staff:
            logger.warning(f"Non-staff user {request.user.username} attempted to create category")
            return Response(
                {'error': 'Only staff users can create categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Category {serializer.data['name']} created by {request.user.username}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        logger.info(f"Category detail accessed for pk {pk} by user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        logger.info(f"Category update attempt for pk {pk} by user: {request.user.username}")
        if not request.user.is_staff:
            logger.warning(f"Non-staff user {request.user.username} attempted to update category {pk}")
            return Response(
                {'error': 'Only staff users can update categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Category {pk} updated by {request.user.username}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        logger.info(f"Category deletion attempt for pk {pk} by user: {request.user.username}")
        if not request.user.is_staff:
            logger.warning(f"Non-staff user {request.user.username} attempted to delete category {pk}")
            return Response(
                {'error': 'Only staff users can delete categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        category = get_object_or_404(Category, pk=pk)
        if category.products.exists():
            return Response(
                {'error': 'Cannot delete category with associated products'},
                status=status.HTTP_400_BAD_REQUEST
            )
        category.delete()
        logger.info(f"Category {pk} deleted by {request.user.username}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        logger.info(f"Product list accessed by user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        logger.info(f"Product creation attempt by user: {request.user.username}")
        if not request.user.is_authenticated:
            logger.warning("Anonymous user attempted to create product")
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Product {serializer.data['name']} created by {request.user.username}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        logger.info(f"Product detail accessed for pk {pk} by user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        logger.info(f"Product update attempt for pk {pk} by user: {request.user.username}")
        if not request.user.is_authenticated:
            logger.warning("Anonymous user attempted to update product")
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Product {pk} updated by {request.user.username}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        logger.info(f"Product deletion attempt for pk {pk} by user: {request.user.username}")
        if not request.user.is_staff:
            logger.warning(f"Non-staff user {request.user.username} attempted to delete product {pk}")
            return Response(
                {'error': 'Only staff users can delete products'},
                status=status.HTTP_403_FORBIDDEN
            )
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        logger.info(f"Product {pk} deleted by {request.user.username}")
        return Response(status=status.HTTP_204_NO_CONTENT)