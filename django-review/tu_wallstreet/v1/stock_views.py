from django.shortcuts import render
from django.forms.models import model_to_dict

from .models import Stocks
from .serializers import StockSerializer
from .permissions import GetNotAuthenticated, isStockAdminGroup

from rest_framework.response import Response
from rest_framework import status, viewsets

class StockViewset(viewsets.ModelViewSet):
    queryset = Stocks.objects.all()
    serializer_class = StockSerializer
    permission_classes = (GetNotAuthenticated, isStockAdminGroup, )