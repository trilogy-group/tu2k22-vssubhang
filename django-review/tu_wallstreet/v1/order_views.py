from django.shortcuts import render
from django.forms.models import model_to_dict

from .models import Orders, Stocks, Users, Holdings, OHLCV, MarketDay
from .serializers import OrderSerializer

from django.db.models import Sum

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated

import datetime

import logging
import multiprocessing

logger = logging.getLogger(__name__)

class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):

        user = Users.objects.filter(email=self.request.user).first()
        return Orders.objects.filter(user=user.id)

    def create(self, request, *args, **kwargs):
        user = Users.objects.filter(email=request.user).first()

        new_data = {**request.data , **{'user': user.id}}

        serializer = OrderSerializer(data=new_data)
        if not serializer.is_valid():
            logger.error("400 Bad Request")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        market_day = MarketDay.objects.filter(status="open")
        if not len(market_day):
            logger.error("403 Forbidden")
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        user = Users.objects.filter(email=request.user).first()

        if serializer.validated_data['type'] == "BUY":
            if serializer.validated_data['bid_price'] * serializer.validated_data['bid_volume'] > user.available_funds:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif serializer.validated_data['type'] == 'SELL':
            holding_list = Holdings.objects.filter(user_id=user.id, stock_id=serializer.validated_data['stock'])
            stock_list = holding_list.aggregate(total_sum=Sum('volume'))
            
            if stock_list['total_sum'] == None or stock_list['total_sum'] < serializer.validated_data['bid_volume']:
                logger.error("400 Bad Request")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error("400 Bad Request")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.validated_data['type'] == "BUY":
            user.available_funds -= serializer.validated_data['bid_price'] * serializer.validated_data['bid_volume']
            user.blocked_funds += serializer.validated_data['bid_price'] * serializer.validated_data['bid_volume']
            user.save()
        
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        user = Users.objects.filter(email=request.user).first()
        order = Orders.objects.filter(id=pk)
        serializer = OrderSerializer(order)
        if not order.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        order = order.first()
        user.available_funds += order.bid_price * order.bid_volume
        user.blocked_funds -= order.bid_price * order.bid_volume

        user.save()
        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def async_process_match(buy_orders_all, sell_orders_all):
        for buy_order in buy_orders_all:
            if buy_order.status == "COMPLETED":
                continue
            for sell_order in sell_orders_all:
                current_date = datetime.datetime.now()
                if buy_order.stock != sell_order.stock or buy_order.bid_price < sell_order.bid_price or sell_order.status == "COMPLETED" or buy_order.user == sell_order.user:
                    continue
                stock_exchanged = min(buy_order.bid_volume - buy_order.executed_volume, sell_order.bid_volume - sell_order.executed_volume)

                selling_holdings = Holdings.objects.filter(stock_id=buy_order.stock.id, user_id=sell_order.user.id)
                temp_amount = stock_exchanged
                for holding in selling_holdings:
                    if temp_amount <= 0:
                        break
                    if holding.volume <= temp_amount:
                        temp_amount -= holding.volume
                        holding.bought_on = current_date
                        holding.user_id = buy_order.user
                        holding.save()
                    else:
                        holding.volume -= temp_amount
                        holding.save()
                        temp_amount = 0
                        break
                
                stock_exchanged -= temp_amount
                if not stock_exchanged:
                    continue
                
                buy_order.executed_volume += stock_exchanged
                sell_order.executed_volume += stock_exchanged

                if buy_order.executed_volume == buy_order.bid_volume:
                    buy_order.status = "COMPLETED"
                if sell_order.executed_volume == sell_order.bid_volume:
                    sell_order.status = "COMPLETED"

                buy_order.updated_at = current_date
                sell_order.updated_at = current_date

                buyer = Users.objects.filter(id=buy_order.user.id).first()
                seller = Users.objects.filter(id=sell_order.user.id).first()

                if buy_order.created_at < sell_order.created_at:
                    stock_price = sell_order.bid_price
                else:
                    stock_price = buy_order.bid_price

                buyer.available_funds += stock_exchanged * (buy_order.bid_price - stock_price)
                buyer.blocked_funds -= buy_order.bid_price * stock_exchanged
                seller.available_funds += stock_price * stock_exchanged

                new_holding = Holdings(volume=stock_exchanged,stock_id=buy_order.stock, bid_price=stock_price, bought_on=current_date, user_id=buy_order.user)
                
                new_day = MarketDay.objects.order_by("day").last()
                record = OHLCV.objects.filter(market_id=new_day.id, stock_id=sell_order.stock.id)

                if record.exists():
                    record = record.first()
                    record.close_price = stock_price
                    record.high_price = max(record.high_price, stock_price)
                    record.low_price = min(record.low_price, stock_price)
                    record.volume += stock_exchanged
                    record.save()
                else:
                    new_record = OHLCV(open_price=stock_price, close_price=stock_price, high_price=stock_price, low_price=stock_price, volume=stock_exchanged, stock_id=buy_order.stock, market_id=new_day) 
                    new_record.save()
                
                buy_order.save()
                sell_order.save()
                buyer.save()
                seller.save()
                new_holding.save()
        
        for buy_order in buy_orders_all:
            current_date = datetime.datetime.now()
            if buy_order.status == "COMPLETED":
                continue
            stock = Stocks.objects.filter(id=buy_order.stock.id).first()
            stock_exchanged = min(buy_order.bid_volume - buy_order.executed_volume, stock.unallocated)
            stock_price = buy_order.bid_price
            if stock_price < stock.price:
                continue

            buyer = Users.objects.filter(id=buy_order.user.id).first()
            stock.price = stock_price
            stock.unallocated -= stock_exchanged
            buy_order.executed_volume += stock_exchanged
            buyer.blocked_funds -= stock_price * stock_exchanged
            buy_order.updated_at = current_date
            if buy_order.executed_volume == buy_order.bid_volume:
                buy_order.status = "COMPLETED"

            new_holding = Holdings(volume=stock_exchanged,stock_id=buy_order.stock, bid_price=stock_price, bought_on=current_date, user_id=buy_order.user)
            

            new_day = MarketDay.objects.order_by("day").last()
            record = OHLCV.objects.filter(market_id=new_day.id, stock_id=buy_order.stock.id)

            if record.exists():
                record = record.first()
                record.close_price = stock_price
                record.high_price = max(record.high_price, stock_price)
                record.low_price = min(record.low_price, stock_price)
                record.volume += stock_exchanged
                record.save()
            else:
                new_record = OHLCV(open_price=stock_price, close_price=stock_price, high_price=stock_price, low_price=stock_price, volume=stock_exchanged, stock_id=buy_order.stock, market_id=new_day) 
                new_record.save()

            buyer.save()
            new_holding.save()
            stock.save()
            buy_order.save()

    @action(detail=False, methods=['post'])
    def match(self, request):
        orders_all = Orders.objects.all()
        
        buy_orders_all = orders_all.filter(type="BUY", status="PENDING").order_by("-bid_price")
        sell_orders_all = orders_all.filter(type="SELL", status="PENDING").order_by("bid_price")
        
        stocks = Stocks.objects.all()

        processors = []

        for stock in stocks:
            buy_stock_order = buy_orders_all.filter(id=stock.id)
            sell_stock_order = sell_orders_all.filter(id=stock.id)
            p = multiprocessing.Process(target=async_process_match, args=(buy_stock_order, sell_stock_order))
            processors.append(p)
            p.start()

        for i in range(len(processors)):
            processors[i].join()
        

        return Response(status=status.HTTP_200_OK)