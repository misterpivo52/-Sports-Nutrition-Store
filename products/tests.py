import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Brand, Category, Product

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        is_staff=True
    )


@pytest.fixture
def brand():
    return Brand.objects.create(name='Test Brand')


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category')


@pytest.fixture
def product(brand, category):
    return Product.objects.create(
        name='Existing Product',
        brand=brand,
        category=category,
        description='Existing description',
        price='39.99'
    )


@pytest.fixture
def product_data(brand, category):
    return {
        'name': 'Test Product',
        'brand': brand.id,
        'category': category.id,
        'description': 'Test description',
        'price': '29.99',
        'image': 'https://example.com/image.jpg'
    }


@pytest.mark.django_db
class TestProductAPI:
    def test_get_products_anonymous(self, api_client, product):
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK

    def test_get_product_detail_anonymous(self, api_client, product):
        response = api_client.get(f'/api/products/{product.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_product_authenticated(self, api_client, user, product_data):
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/products/', product_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_product_anonymous(self, api_client, product_data):
        response = api_client.post('/api/products/', product_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_product_authenticated(self, api_client, user, product):
        api_client.force_authenticate(user=user)
        update_data = {'name': 'Updated Product'}
        response = api_client.put(f'/api/products/{product.id}/', update_data)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_product_staff(self, api_client, admin_user, product):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/api/products/{product.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_non_staff(self, api_client, user, product):
        api_client.force_authenticate(user=user)
        response = api_client.delete(f'/api/products/{product.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_product_invalid_data(self, api_client, user):
        api_client.force_authenticate(user=user)
        invalid_data = {'name': ''}
        response = api_client.post('/api/products/', invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_nonexistent_product(self, api_client):
        response = api_client.get('/api/products/999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_product(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete('/api/products/999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBrandAPI:
    def test_get_brands_anonymous(self, api_client, brand):
        response = api_client.get('/api/brands/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_brand_staff(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/api/brands/', {'name': 'New Brand'})
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_brand_non_staff(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/brands/', {'name': 'New Brand'})
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCategoryAPI:
    def test_get_categories_anonymous(self, api_client, category):
        response = api_client.get('/api/categories/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_category_staff(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/api/categories/', {'name': 'New Category'})
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_category_non_staff(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/categories/', {'name': 'New Category'})
        assert response.status_code == status.HTTP_403_FORBIDDEN