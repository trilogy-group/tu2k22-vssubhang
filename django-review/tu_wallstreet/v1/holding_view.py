from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import F, Sum

from .models import Holdings, Users

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class HoldingView(APIView):
    def get(self, request):
        # Authenticate the user and get user_id
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        user_id = Users.objects.filter(email=request.user).first().id

        holding_list = Holdings.objects.filter(user_id=user_id)

        stock_list = holding_list.values('stock_id', 'stock_id__name', 'stock_id__price').annotate(total_bid_price=Sum(F('volume') * F('bid_price')), total_volume=Sum(F('volume'))).order_by('stock_id')
        if len(stock_list):
            stock_current_value = stock_list.aggregate( investment=Sum(F('total_bid_price')), current_value=Sum(F('stock_id__price') * F('total_volume')))
        else:
            stock_current_value = {'investment': 0.00, 'current_value': 0.00}
        stocks_possessed = []
        for stock in stock_list:
            stocks_possessed.append({'id' : stock['stock_id'], 'name' : stock['stock_id__name'], 'total_volume': int(stock['total_volume']), 'avg_bid_price' : "{:.2f}".format(float(stock['total_bid_price'])/stock['total_volume'])})
       
        return Response(data={'investment': "{:.2f}".format(stock_current_value['investment']), 'current_value': "{:.2f}".format(stock_current_value['current_value']), 'stocks_possessed': stocks_possessed}, status=status.HTTP_200_OK)
