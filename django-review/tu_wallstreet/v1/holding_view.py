from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import F, Sum

from .models import Holdings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class HoldingView(APIView):
    def get(self, request):
        # Authenticate the user and get user_id
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        user_id = request.user.id
        holding_list = Holdings.objects.filter(user_id=user_id)

        stock_list = holding_list.values('stock_id', 'stock_id__name', 'stock_id__price').annotate(avg_bid_price=Sum(F('volume') * F('bid_price')) / Sum(F('volume')), total_volume=Sum(F('volume'))).order_by('stock_id')
        if len(stock_list):
            stock_current_value = stock_list.aggregate( investment=Sum(F('avg_bid_price') * F('total_volume')), current_value=Sum(F('stock_id__price') * F('total_volume')))
        else:
            stock_current_value = {'investment': 0.0, 'current_value': 0.0}
        stocks_possessed = []
        for stock in stock_list:
            stocks_possessed.append({'id' : stock['stock_id'], 'name' : stock['stock_id__name'], 'total_volume': int(stock['total_volume']), 'avg_bid_price' : float(stock['avg_bid_price'])})
        print({'investment': stock_current_value['investment'], 'current_value': stock_current_value['current_value'], 'stocks_possesed': stocks_possessed})
        return Response(data={'investment': float(stock_current_value['investment']), 'current_value': float(stock_current_value['current_value']), 'stocks_possesed': stocks_possessed}, status=status.HTTP_200_OK)
