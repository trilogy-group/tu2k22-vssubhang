from django.test import TestCase

from rest_framework.test import APIClient

# Create your tests here.

class OrdersBuyTests(TestCase):
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

        sector_data = {"name": "Sector 1", "description": "Good Sector"}
        resposne = self.client.post("/api/v1/sectors/", data=sector_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        stock_data = {"name": "Stock 1", "price": 10, "sector": 1, "unallocated": 100, "total_volume": 100}
        resposne = self.client.post("/api/v1/stocks/", data=stock_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        stock_data = {"name": "Stock 2", "price": 20, "sector": 1, "unallocated": 100, "total_volume": 100}
        resposne = self.client.post("/api/v1/stocks/", data=stock_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

    def test_order_fail_market_close(self):
        order_data = {"stock": 1, "type":"BUY", "bid_price": 200, "bid_volume": 3}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 403)

    def test_order_fail_empty_type(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "bid_price": 200, "bid_volume": 3}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 400)

    def test_order_fail_empty_volume(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_price": 200}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 400)

    def test_order_fail_empty_stock(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"type":"BUY", "bid_price": 200, "bid_volume": 3}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 400)

    def test_order_fail_empty_price(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_volume": 3}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 400)

    def test_order_fail_insufficient_funds(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_price": 20000000, "bid_volume": 3}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 400)

    def test_order_fail_insufficient_stocks(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"SELL", "bid_price": 20000000.00, "bid_volume": 25}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 400)

    def test_order_fail_invalid_type(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"HOLD", "bid_price": 20000000.00, "bid_volume": 25}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 400)

    def test_order_success(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_volume": 3, "bid_price": 40}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        assert(response.status_code == 201)
    
    def test_order_delete_fail_invalid_id(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_volume": 3, "bid_price": 40}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")
        assert(response.status_code == 201)

        response = self.client.delete("/api/v1/orders/8/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")
        assert(response.status_code == 404)

    def test_order_delete_success(self):
        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_volume": 3, "bid_price": 40}
        response = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token, format="json")
        assert(response.status_code == 201)

        response = self.client.delete("/api/v1/orders/1/", HTTP_AUTHORIZATION = "Token " + self.token, format="json")
        assert(response.status_code == 204)

class MatchesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        self.token = []
        self.token.append(response.data["token"])

        body = {
            "name": "hnag",
            "email": "hang@asas.com",
            "password": "123456"
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        self.token.append(response.data["token"])

        response = self.client.post("/api/v1/market/open/", HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")

        sector_data = {"name": "Sector 1", "description": "Good Sector"}
        resposne = self.client.post("/api/v1/sectors/", data=sector_data, HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")

        stock_data = {"name": "Stock 1", "price": 10, "sector": 1, "unallocated": 100, "total_volume": 100}
        resposne = self.client.post("/api/v1/stocks/", data=stock_data, HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")

        stock_data = {"name": "Stock 2", "price": 20, "sector": 1, "unallocated": 100, "total_volume": 100}
        resposne = self.client.post("/api/v1/stocks/", data=stock_data, HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_price": 200, "bid_volume": 3}
        resposne = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")

    def test_match_order_success_1(self):

        response = self.client.post("/api/v1/orders/match/", HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")
        assert(response.status_code == 200)

    def test_match_order_success_2(self):

        response = self.client.post("/api/v1/orders/match/", HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")
        assert(response.status_code == 200)

        order_data = {"stock": 1, "type":"SELL", "bid_price": 20, "bid_volume": 3}
        resposne = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")

        order_data = {"stock": 1, "type":"BUY", "bid_price": 400, "bid_volume": 4}
        resposne = self.client.post("/api/v1/orders/", data=order_data, HTTP_AUTHORIZATION = "Token " + self.token[1], format="json")

        response = self.client.post("/api/v1/orders/match/", HTTP_AUTHORIZATION = "Token " + self.token[0], format="json")
        assert(response.status_code == 200)