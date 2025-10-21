import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'password_check': 'Test123!'
    }


@pytest.fixture
def user():
    return User.objects.create_user(
        username='existinguser',
        email='existing@example.com',
        password='Existing123!'
    )


@pytest.mark.django_db
class TestAuthenticationAPI:
    def test_register_success(self, api_client, user_data):
        response = api_client.post('/api/auth/register/', user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data

    def test_register_password_mismatch(self, api_client, user_data):
        invalid_data = user_data.copy()
        invalid_data['password_check'] = 'Different123!'
        response = api_client.post('/api/auth/register/', invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, api_client, user_data):
        invalid_data = user_data.copy()
        invalid_data['password'] = 'weak'
        invalid_data['password_check'] = 'weak'
        response = api_client.post('/api/auth/register/', invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, api_client, user):
        login_data = {
            'username': 'existinguser',
            'password': 'Existing123!'
        }
        response = api_client.post('/api/auth/login/', login_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_login_invalid_credentials(self, api_client, user):
        login_data = {
            'username': 'existinguser',
            'password': 'WrongPassword'
        }
        response = api_client.post('/api/auth/login/', login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_profile_authenticated(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_200_OK

    def test_get_profile_unauthenticated(self, api_client):
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED