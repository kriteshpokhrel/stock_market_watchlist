from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, WatchlistDeleteView, WatchlistListCreateView, WatchlistStockPriceView

router = DefaultRouter()
router.register(r'stocks', StockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
    path('watchlist/', WatchlistListCreateView.as_view(), name='watchlist-list-create'),
    path('watchlist/<int:pk>/', WatchlistDeleteView.as_view(), name='watchlist-delete'),
    path('watchlist/<int:pk>/price/', WatchlistStockPriceView.as_view(), name='watchlist-stock-price'),
]
