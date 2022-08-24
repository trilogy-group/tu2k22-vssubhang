from django.shortcuts import render
from django.forms.models import model_to_dict

from .models import Sectors
from .serializers import SectorSerializer
from .permissions import GetNotAuthenticated

from rest_framework.response import Response
from rest_framework import status, viewsets

class SectorViewset(viewsets.ModelViewSet):
    queryset = Sectors.objects.all()
    serializer_class = SectorSerializer
    permission_classes = (GetNotAuthenticated, )
