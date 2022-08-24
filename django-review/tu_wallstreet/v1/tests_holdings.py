from django.test import TestCase

from rest_framework.test import APIClient

# Create your tests here.

class HoldingsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        self.token = response.data["token"]

        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        sector_data = {"name": "Sector 1", "description": "Good Sector"}
        resposne = self.client.post("/api/v1/sectors/", data=sector_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        stock_data = {"name": "Stock 1", "price": 10, "sector": 1, "unallocated": 100, "total_volume": 100}
        resposne = self.client.post("/api/v1/stocks/", data=stock_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        stock_data = {"name": "Stock 2", "price": 20, "sector": 1, "unallocated": 100, "total_volume": 100}
        resposne = self.client.post("/api/v1/stocks/", data=stock_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_price": 200, "bid_volume": 3}
        resposne = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        response = self.client.post("/api/v1/orders/match/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

    def test_get_holdings_fail_unathenticated(self):

        response = self.client.get("/api/v1/holdings/")
        assert(response.status_code == 401)

    def test_get_holdings_success(self):

        response = self.client.get("/api/v1/holdings/", HTTP_AUTHORIZATION = "Token " + self.token)
        assert(response.status_code == 200)
        
        assert(response.data["investment"] == "600.00")
        assert(len(response.data["stocks_possessed"]) == 1)
