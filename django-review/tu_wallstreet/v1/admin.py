from django.contrib import admin
from .models import Stocks, Orders, Holdings, Sectors, OHLCV, MarketDay, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Stocks)
admin.site.register(Orders)
admin.site.register(Holdings)
admin.site.register(Sectors)
admin.site.register(OHLCV)
admin.site.register(MarketDay)