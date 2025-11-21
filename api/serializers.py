import re
from rest_framework import serializers
from .models import Stock, Watchlist
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model."""

    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'name', 'price', 'last_updated']

        def validate_symbol(self, value):
            # Must be uppercase alphanumeric between 1 to 10 chars
            if not re.match(r'^[A-Z0-9]{1,10}$', value):
                raise serializers.ValidationError("Invalid stock symbol. Must be uppercase alphanumeric, max 10 characters.")
            return value.upper()  # normalize to uppercase
    
        def update(self, instance, validated_data):
            # Prevent update of fields other than price and last_updated
            if 'symbol' in validated_data or 'name' in validated_data:
                raise serializers.ValidationError("Only price update is allowed.")
            return super().update(instance, validated_data)

class WatchlistSerializer(serializers.ModelSerializer):
    """Serializer for Watchlist model."""

    stock = StockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(), source='stock', write_only=True
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'stock', 'stock_id', 'added_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user