from django.shortcuts import render
from django.forms.models import model_to_dict

from .models import MarketDay, OHLCV, Stocks
from .serializers import MarketSerializer, OHLCVSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.


class OpenMarketView(APIView):
    def post(self, request, *args, **kwargs):
        open_days_count = MarketDay.objects.filter(status="open").count()
        if open_days_count:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                previous_day = model_to_dict(MarketDay.objects.latest('day'))['day']
            except:
                previous_day = 0
            serializer = MarketSerializer(data = {'status':"open", 'day':previous_day + 1})
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CloseMarketView(APIView):
    def post(self, request, *args, **kwargs):
        open_days_count = MarketDay.objects.filter(status="open").count()
        if open_days_count != 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            current_day = MarketDay.objects.latest('day')
            current_day.status = "closed"
            current_day.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

class OHLCVView(APIView):
    def get(self, request):
        try:
            selected_day = int(request.query_params['day'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        market_day = MarketDay.objects.filter(day=selected_day)[0]
        stock_list = Stocks.objects.all()
        response = []
        for stock in stock_list:
            record = OHLCV.objects.filter(market_id=market_day.id, stock_id=stock.id)

            if record.exists():
                record = record.first()
                pass
            else:
                record = OHLCV(open_price=-1, close_price=-1, high_price=-1, low_price=-1, volume=0, market_id=market_day, stock_id=stock)
                record.save()
            response.append({'open': record.open_price, 'close': record.close_price, 'low': record.low_price, 'high': record.high_price, 'day': market_day.day, 'stock': stock.name, 'volume': record.volume})

        return Response(response, status=status.HTTP_200_OK)

class CircuitSlashDevflow(APIView):
    def get(select, request):
        
        market_day = MarketDay.objects.order_by("day")

        if not market_day.exists():
            return Response({"message":"Something went wrong please try later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        market_day = market_day.last()

        stock_list = Stocks.objects.all()
        response = {"message":"No stocks traded today or crossed the circuit limit"}
        circuit_list = []
        for stock in stock_list:
            record = OHLCV.objects.filter(market_id=market_day.id, stock_id=stock.id)
            if record.exists() and record.first().open_price != -1:
                record = record.first()
                if (stock.price - record.open_price) / record.open_price >= 0.1:
                    circuit_list.append(stock.name+"(Gain)")
                elif abs(stock.price - record.open_price) / record.open_price >= 0.1:
                    circuit_list.append(stock.name+"(Loss)")
                print(stock.price, record.open_price)
        if len(circuit_list):
            return Response({"message": "The following stocks crossed their limits " + ",".join(circuit_list)}, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_200_OK)
