from django.db import models
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=50, null=False, blank=False, unique=True)
    password = models.CharField(max_length=50, null=False, blank=False)
    available_funds = models.DecimalField(max_digits=10, decimal_places=2, default=400000)
    blocked_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Sectors(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)


class MarketDay(models.Model):
    day = models.IntegerField()
    status = models.CharField(max_length=10)


class Stocks(models.Model):
    name = models.CharField(max_length=20)
    total_volume = models.IntegerField()
    unallocated = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    sector = models.ForeignKey(Sectors, on_delete=models.CASCADE)


class OHLCV(models.Model):
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()

    market_id = models.ForeignKey(MarketDay, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stocks, on_delete=models.CASCADE)


class Orders(models.Model):
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_volume = models.IntegerField()
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=4)
    executed_volume = models.IntegerField(default=0)

    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)


class Holdings(models.Model):
    volume = models.IntegerField()
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    bought_on = models.DateField()

    stock_id = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
