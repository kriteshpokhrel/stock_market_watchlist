from rest_framework import status
from django.utils import timezone
from django.urls import reverse
from .base_setup import BaseAPITestCase
from ..models import Stock, Watchlist

class WatchlistAPITestCase(BaseAPITestCase):
    """ Test suite for Watchlist API endpoints. """

    def setUp(self):
        super().setUp()
        # ARRANGE: Create sample stocks
        self.stock1 = Stock.objects.create(symbol='AAPL', name='Apple Inc.', price=150.00, last_updated=timezone.now())
        self.stock2 = Stock.objects.create(symbol='GOOGL', name='Alphabet Inc.', price=2800.00, last_updated=timezone.now())

        # ARRANGE: Create watchlist entry for regular user
        self.watchlist_entry = Watchlist.objects.create(user=self.regular_user, stock=self.stock1)

        # ARRANGE: Authenticate as regular user
        self.authenticate(self.regular_user)

    def test_add_stock_to_watchlist(self):
        """Test adding a new stock to the watchlist."""
        # ARRANGE
        url = reverse('watchlist-list-create')
        data = {'stock_id': self.stock2.id}
        # ACT
        response = self.client.post(url, data)
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Watchlist.objects.filter(user=self.regular_user, stock=self.stock2).exists())

    def test_prevent_duplicate_watchlist_entry(self):
        """Test that adding a stock already in the watchlist returns a 400 error."""
        # ARRANGE
        url = reverse('watchlist-list-create')
        data = {'stock_id': self.stock1.id}
        # ACT
        response = self.client.post(url, data)
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Stock already in watchlist.', str(response.data))

    def test_delete_watchlist_entry(self):
        """Test deleting a watchlist entry."""
        # ARRANGE
        url = reverse('watchlist-delete', args=[self.watchlist_entry.id])
        # ACT
        response = self.client.delete(url)
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Watchlist.objects.filter(id=self.watchlist_entry.id).exists())

    def test_retrieve_latest_price(self):
        """Test retrieving the latest price of a stock in the watchlist."""
        # ARRANGE
        url = reverse('watchlist-stock-price', args=[self.watchlist_entry.id])
        # ACT
        response = self.client.get(url)
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'AAPL')
        self.assertEqual(float(response.data['latest_price']), float(self.stock1.price))

    def test_auth_required(self):
        """Test that authentication is required to access the watchlist."""
        # ARRANGE
        self.client.logout()
        url = reverse('watchlist-list-create')
        # ACT
        response = self.client.get(url)
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
