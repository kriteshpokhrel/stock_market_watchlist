from rest_framework import viewsets, permissions, filters, status
from .models import Stock, Watchlist
from rest_framework import generics, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StockSerializer, WatchlistSerializer, UserRegistrationSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.authtoken.views import ObtainAuthToken

# Stock API
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['symbol', 'name']
    ordering_fields = ['price', 'name']
    ordering = ['name']

    def get_permissions(self):
        """
        Only superusers can create or update stocks.
        All other actions are public (read-only).
        """
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        """
        PATCH /api/stocks/{id}/
        Update the price of a stock. Only 'price' is allowed.
        """
        price = request.data.get("price")
        if price is None:
            raise serializers.ValidationError({
                "price": "Only 'price' can be updated and it is required."
            })

        instance = self.get_object()
        instance.price = price
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# Watchlist API
class WatchlistListCreateView(generics.ListCreateAPIView):
    """
    GET /watchlist/       : List authenticated user's watchlist
    POST /watchlist/      : Add a stock to the watchlist
    """
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only watchlist entries for the authenticated user"""
        return Watchlist.objects.filter(user=self.request.user).select_related('stock')

    def perform_create(self, serializer):
        """Add a stock to the user's watchlist, preventing duplicates"""
        stock = serializer.validated_data['stock']
        if Watchlist.objects.filter(user=self.request.user, stock=stock).exists():
            raise serializers.ValidationError("Stock already in watchlist.")
        serializer.save(user=self.request.user)


class WatchlistDeleteView(generics.DestroyAPIView):
    """
    DELETE /watchlist/{id}/
    Delete a watchlist entry belonging to the authenticated user.
    """
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)


class WatchlistStockPriceView(APIView):
    """
    GET /watchlist/{id}/price/
    Retrieve the latest price of a stock in the user's watchlist.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk, user=request.user)
        except Watchlist.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        stock = watchlist.stock
        return Response({
            'symbol': stock.symbol,
            'name': stock.name,
            'latest_price': stock.price,
            'last_updated': stock.last_updated
        })


# User Authentication & Registration
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        headers = self.get_success_headers(serializer.data)
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": getattr(user, 'name', ''),
        }
        return Response(user_data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(ObtainAuthToken):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
