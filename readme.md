
# Sports Nutrition Store

## Description

A Django REST API for sports nutrition products store with JWT authentication. Users can view products, register, login, and manage products with proper authorization.

## Features

- **User Authentication**: JWT-based registration and login
- **Product Management**: CRUD operations for products
- **Brand & Category Management**: Organize products by brands and categories  
- **Authorization**: Different access levels for anonymous users, authenticated users, and staff
- **Filtering**: Filter products by brand and category
- **Testing**: Comprehensive test coverage with pytest

---

## API Endpoints

### Authentication

#### Register
- **What it does**: Create new user account
- **Method**: `POST`
- **URL**: `/api/auth/register/`
- **Send**:
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "SecurePass123",
  "password_check": "SecurePass123"
}
```
- **Response**:
```json
{
  "user": {
    "id": 1,
    "username": "john",
    "first_name": "",
    "last_name": "", 
    "email": "john@example.com"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Login
- **What it does**: Login to account
- **Method**: `POST`
- **URL**: `/api/auth/login/`
- **Send**:
```json
{
  "username": "john",
  "password": "SecurePass123"
}
```
- **Response**: Same as register response

#### Get Profile
- **What it does**: Show my user info
- **Method**: `GET`
- **URL**: `/api/auth/profile/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
```json
{
  "id": 1,
  "username": "john",
  "first_name": "",
  "last_name": "",
  "email": "john@example.com"
}
```

#### Refresh Token
- **What it does**: Get new access token
- **Method**: `POST`
- **URL**: `/api/auth/token/refresh/`
- **Send**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Response**: New access token

#### Logout
- **What it does**: Logout from account
- **Method**: `POST`
- **URL**: `/api/auth/logout/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Send**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Response**: Success message

---

### Products

#### Get all products
- **What it does**: Shows list of all products
- **Method**: `GET`
- **URL**: `/api/products/`
- **Access**: Public
- **Response**:
```json
[
  {
    "id": 1,
    "name": "Whey Protein",
    "brand": 1,
    "brand_name": "Optimum Nutrition",
    "category": 1,
    "category_name": "Protein",
    "description": "High quality protein powder",
    "price": "45.99",
    "image": "http://example.com/image.jpg",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Get one product
- **What it does**: Shows details of one product
- **Method**: `GET`
- **URL**: `/api/products/1/`
- **Access**: Public
- **Response**: Single product object

#### Create product
- **What it does**: Add new product
- **Method**: `POST`
- **URL**: `/api/products/`
- **Access**: Authenticated users
- **Headers**: `Authorization: Bearer <access_token>`
- **Send**:
```json
{
  "name": "BCAA",
  "brand": 1,
  "category": 2,
  "description": "Essential amino acids",
  "price": "29.99",
  "image": "http://example.com/bcaa.jpg"
}
```
- **Response**: Created product

#### Update product
- **What it does**: Change product info
- **Method**: `PUT` / `PATCH`
- **URL**: `/api/products/1/`
- **Access**: Authenticated users
- **Headers**: `Authorization: Bearer <access_token>`
- **Send**: Same as create
- **Response**: Updated product

#### Delete product
- **What it does**: Remove product
- **Method**: `DELETE`
- **URL**: `/api/products/1/`
- **Access**: Staff users only
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Nothing (just success)

---

### Brands

#### Get all brands
- **What it does**: Shows all brands
- **Method**: `GET`
- **URL**: `/api/brands/`
- **Access**: Public
- **Response**:
```json
[
  {
    "id": 1,
    "name": "Optimum Nutrition",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Create brand
- **What it does**: Add new brand
- **Method**: `POST`
- **URL**: `/api/brands/`
- **Access**: Staff users only
- **Headers**: `Authorization: Bearer <access_token>`
- **Send**:
```json
{
  "name": "New Brand"
}
```
- **Response**: Created brand

---

### Categories

#### Get all categories
- **What it does**: Shows all categories
- **Method**: `GET`
- **URL**: `/api/categories/`
- **Access**: Public
- **Response**:
```json
[
  {
    "id": 1,
    "name": "Protein",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Create category
- **What it does**: Add new category
- **Method**: `POST`
- **URL**: `/api/categories/`
- **Access**: Staff users only
- **Headers**: `Authorization: Bearer <access_token>`
- **Send**:
```json
{
  "name": "New Category"
}
```
- **Response**: Created category

---

## Permissions

### Public endpoints (no authentication required):
- `GET /api/products/`, `GET /api/products/{id}/`
- `GET /api/brands/`, `GET /api/categories/`
- `POST /api/auth/register/`, `POST /api/auth/login/`

### Authenticated users only:
- `POST /api/products/` (create products)
- `PUT/PATCH /api/products/{id}/` (update products)
- `GET /api/auth/profile/`, `POST /api/auth/logout/`

### Staff users only:
- `POST /api/brands/`, `POST /api/categories/`
- `DELETE /api/products/{id}/`, `DELETE /api/brands/{id}/`, `DELETE /api/categories/{id}/`

---

## Database Schema

### Models:

**CustomUser**
- id
- username
- email
- password
- first_name
- last_name
- is_staff
- is_superuser
- date_joined

**Brand**
- id
- name
- created_at

**Category**
- id
- name
- created_at

**Product**
- id
- name
- brand (ForeignKey to Brand)
- category (ForeignKey to Category)
- description
- price
- image
- created_at
- updated_at

---

## Technology Stack

- **Backend**: Django 5.2.6, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite
- **Testing**: pytest, pytest-django, coverage
- **CORS**: django-cors-headers

---

## Installation & Setup

### 1. Clone repository:
```bash
git clone <repository-url>
cd sports-nutrition-store
```

### 2. Create virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

### 6. Seed database with sample data:
```bash
python seed_data.py
```

### 7. Run development server:
```bash
python manage.py runserver
```

---

## Testing

### Run tests with pytest:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific app tests
pytest products/
pytest authentication/

# Generate HTML coverage report
pytest --cov --cov-report=html
```

### Current Test Coverage: 85%
- Authentication tests: 100%
- Products tests: 100%
- Overall coverage: 85% (511 statements, 78 missed)

---

## Frontend Integration

A simple frontend is available in `index.html` that demonstrates:
- User registration and login
- Product listing with brand/category filters
- Product creation (authenticated users)
- JWT token management

### To use the frontend:
1. Start the Django server
2. Open `index.html` in a web browser
3. The frontend will communicate with the API via CORS

---


