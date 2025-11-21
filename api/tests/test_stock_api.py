from rest_framework import status
from django.utils import timezone
from ..models import Stock
from .base_setup import BaseAPITestCase

class StockAPITests(BaseAPITestCase):
    """ Test suite for Stock API endpoints. """

    def setUp(self):
        super().setUp()
        # ARRANGE: Create sample stocks
        Stock.objects.create(symbol='AAPL', name='Apple Inc.', price=150.00, last_updated=timezone.now())
        Stock.objects.create(symbol='GOOGL', name='Alphabet Inc.', price=2800.50, last_updated=timezone.now())
        Stock.objects.create(symbol='TSLA', name='Tesla Inc.', price=700.75, last_updated=timezone.now())

    def test_list_stocks_without_filters(self):
        """Test listing all stocks without applying any filters."""
        # ACT
        response = self.client.get('/api/stocks/')
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_stocks_by_symbol(self):
        """Test filtering stocks by their symbol."""
        # ACT
        response = self.client.get('/api/stocks/', {'symbol': 'AAPL'})
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['symbol'], 'AAPL')

    def test_filter_stocks_by_name(self):
        """Test filtering stocks by their name."""
        # ACT
        response = self.client.get('/api/stocks/', {'name': 'Tesla Inc.'})
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Tesla Inc.')

    def test_sort_stocks_by_price_desc(self):
        """Test sorting stocks by price in descending order."""
        # ACT
        response = self.client.get('/api/stocks/', {'ordering': '-price'})
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['symbol'], 'GOOGL')

    def test_retrieve_stock_detail(self):
        """Test retrieving details of a single stock by ID."""
        # ARRANGE
        stock = Stock.objects.get(symbol='AAPL')
        # ACT
        response = self.client.get(f'/api/stocks/{stock.id}/')
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'AAPL')

    def test_create_stock_as_superuser(self):
        """Test that a superuser can create a new stock."""
        # ARRANGE
        self.authenticate(self.admin_user)
        data = {
            'symbol': 'MSFT',
            'name': 'Microsoft Corporation',
            'price': 300.00
        }
        # ACT
        response = self.client.post('/api/stocks/', data)
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stock.objects.count(), 4)

    def test_create_stock_as_regular_user_denied(self):
        """Test that a regular user cannot create a new stock."""
        # ARRANGE
        self.authenticate(self.regular_user)
        data = {
            'symbol': 'AMZN',
            'name': 'Amazon.com Inc.',
            'price': 3300.00
        }
        # ACT
        response = self.client.post('/api/stocks/', data)
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_stock_price_as_superuser(self):
        """Test that a superuser can update the price of a stock."""
        # ARRANGE
        stock = Stock.objects.get(symbol='AAPL')
        self.authenticate(self.admin_user)
        # ACT
        response = self.client.patch(
            f'/api/stocks/{stock.id}/',
            {'price': 155.00},
            format='json'
        )
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stock.refresh_from_db()
        self.assertEqual(stock.price, 155.00)

    def test_update_stock_price_as_regular_user_denied(self):
        """Test that a regular user cannot update a stock price."""
        # ARRANGE
        stock = Stock.objects.get(symbol='AAPL')
        self.authenticate(self.regular_user)
        # ACT
        response = self.client.patch(
            f'/api/stocks/{stock.id}/',
            {'price': 155.00},
            format='json'
        )
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
