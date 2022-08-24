from django.test import TestCase

from rest_framework.test import APIClient

# Create your tests here.

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_signup_fail_empty_name(self):
        body = {
            "email": "Subhang@asas.com",
            "password": "123456"
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 400)
    
    def test_user_signup_fail_empty_email(self):
        body = {
            "name": "Subhang",
            "password": "123456"
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 400)
    
    def test_user_signup_fail_empty_password(self):
        body = {
            "email": "Subhang@asas.com",
            "name": "123456"
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 400)

    def test_user_signup_fail_empty_all(self):
        body = {
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 400)

    def test_user_signup_fail_email_invalid(self):
        body = {
            "email": "123456",
            "name": "subhang",
            "password": "123456"
        }
        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 400)

    def test_user_signup_success(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

    def test_user_login_fail_empty_email(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        body = {
            "password": "123456"
        }
        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 400)
    
    def test_user_login_fail_empty_passordl(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        body = {
            "email": "123456@1234.com"
        }
        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 400)

    def test_user_login_fail_invalid_email(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        body = {
            "email": "123456",
            "password": "12qwaszx"
        }
        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 400)

    def test_user_login_fail_invalid_credentials(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        body = {
            "email": "123456@1243.com",
            "password": "12qwaszx"
        }
        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 400)

    def test_user_login_success(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 200)

    def test_user_logout_fail_not_authenticated(self):

        response = self.client.post('/api/v1/auth/logout/')
        assert(response.status_code == 401)

    def test_user_logout_fail_invalid_token(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 200)

        token = "12341234"

        response = self.client.post('/api/v1/auth/logout/', HTTP_AUTHORIZATION = "Token " + token)
        assert(response.status_code == 401)

    def test_user_logout_success(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 200)

        token = response.data["token"]

        response = self.client.post('/api/v1/auth/logout/', HTTP_AUTHORIZATION = "Token " + token)
        assert(response.status_code == 204)

    def test_get_user_details_fail_unauthenticated(self):
        
        response = self.client.get('/api/v1/users/profile/')
        assert(response.status_code == 401)

    def test_get_user_details_success(self):
        body = {
            "name": "subhnag",
            "email": "Subhang@asas.com",
            "password": "123456"
        }

        response = self.client.post("/api/v1/auth/signup/", data=body, format="json")
        assert(response.status_code == 201)

        response = self.client.post("/api/v1/auth/login/", data=body, format="json")
        assert(response.status_code == 200)

        token = response.data["token"]
        
        response = self.client.get('/api/v1/users/profile/', HTTP_AUTHORIZATION = "Token " + token)
        assert(response.status_code == 200)