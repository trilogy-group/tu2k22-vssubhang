"""tu_wallstreet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_nested import routers

from .market_views import OpenMarketView, CloseMarketView, OHLCVView, CircuitSlashDevflow
from .holding_view import HoldingView
from .sector_views import SectorViewset
from .stock_views import StockViewset
from .order_views import OrderViewset
from .user_views import SignupView, LoginView, LogoutView, UserViewset, GithubLogin, DevflowsCallback

delete_order = OrderViewset.as_view({
    'delete': 'destroy'
})

router = routers.SimpleRouter()
router.register(r'sectors', SectorViewset)
router.register(r'stocks', StockViewset)
router.register(r'orders', OrderViewset, basename='OrderViewSet')
router.register(r'users/profile', UserViewset, basename='UserViewSet')

urlpatterns = [
    path('market/open/', OpenMarketView.as_view()),
    path('market/close/', CloseMarketView.as_view()),
    path('market/ohlc/', OHLCVView.as_view()),
    path('market/circuit/', CircuitSlashDevflow.as_view()),
    path('holdings/', HoldingView.as_view()),
    path('auth/signup/', SignupView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('orders/<int:pk>/cancel/', delete_order),
    path('github-login/', GithubLogin.as_view()),
    path('callback', DevflowsCallback.as_view()),
    path('', include(router.urls))
]