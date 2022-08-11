from rest_framework import serializers
from .models import MarketDay, OHLCV, Stocks, Sectors, Orders, Users
from django.db import models

import re

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketDay
        fields = '__all__'

class OHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = OHLCV
        fields = '__all__'

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'email', 'password']

    def validate(self, value):
        if not value['email'] or not value['password']:
            raise serializers.ValidationError("No email provided")
        if not re.match(r"^\S+@\S+\.\S+$", value['email']):
            raise serializers.ValidationError("Not correct email")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
