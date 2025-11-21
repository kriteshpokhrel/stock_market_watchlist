# Stock Market Watchlist API

A RESTful API built with Django and Django REST Framework for tracking stock prices and managing your personal watchlist. This project is designed for easy integration, extension, and maintenance according to Django best practices.

***

## Features

- User Registration \& Authentication (secure endpoints with Token)
- Detailed Stock Listing
- Watchlist Management (add, remove stocks, view latest price)
- Admin Control for stock creation \& price updates
- Input validation \& error handling

***

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Testing](#testing)

***

## Installation

1. **Clone the repo:**

```
git clone https://github.com/yourusername/stock-watchlist-api.git
cd stock-watchlist-api
```

2. **Set up virtual environment:**

```
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```
pip install -r requirements.txt
```

4. **Configure environment variables:**
    - Create a `.env` file and set up your secret key, DB config, JWT settings.
5. **Run migrations:**

```
python manage.py migrate
```

6. **Create a superuser:**

```
python manage.py createsuperuser
```

7. **Start the server:**

```
python manage.py runserver
```

***

## Setup

- PostgreSQL is the default database (configure in `settings.py`)
- All authentication uses Token-based mechanisms

***

## Authentication

- Register via `/api/register/`
- Login via `/api/login/` (returns JWT/Token for authenticated requests)
- Secure endpoints require JWT/Token in `Authorization` header

***

## API Endpoints

| Endpoint | Description | Auth Required |
| :-- | :-- | :-- |
| `/api/register/` | User Registration | No |
| `/api/login/` | User Login (returns token) | No |
| `/api/stocks/` | List all stocks, filter/sort/paginate | No |
| `/api/stocks/{id}/` | Get details of a single stock | No |
| `/api/stocks/` (POST) | Create new stock (superuser only) | Yes |
| `/api/watchlist/` | Get authenticated user's watchlist | Yes |
| `/api/watchlist/` (POST) | Add a stock to watchlist | Yes |
| `/api/watchlist/{id}/` (DELETE)| Remove a stock from watchlist | Yes |
| `/api/watchlist/{id}/price/` | Get latest price of a watched stock | Yes |


***

## Usage Examples

**Register User**

```http
POST /api/register/
{
  "name": "Navya",
  "email": "navya@example.com",
  "password": "yourpassword"
}
```

**Login**

```http
POST /api/login/
{
  "email": "navya@example.com",
  "password": "yourpassword"
}
# Response contains token
```

**List Stocks**

```http
GET /api/stocks/?symbol=AAPL&order_by=price
```

**Add to Watchlist**

```http
POST /api/watchlist/
{
  "stock": 1
}
```


***

- **Testing:**
Unit tests for models, views, and serializers. Tests are located in tests folderRun via:

```
python manage.py api.tests
```


***
