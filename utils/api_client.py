import requests
from utils.api_endpoints import *

class ApiClient:
    @staticmethod
    def register_user(data):
        return requests.post(REGISTER, json=data)
    
    @staticmethod
    def login_user(data):
        return requests.post(LOGIN, json=data)
    
    @staticmethod
    def update_user(headers, data):
        return requests.patch(USER_PROFILE, headers=headers, json=data)
    
    @staticmethod
    def create_order(headers, ingredients):
        return requests.post(ORDERS, headers=headers, json={"ingredients": ingredients})
    
    @staticmethod
    def get_orders(headers):
        return requests.get(ORDERS, headers=headers)