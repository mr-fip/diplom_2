import allure
import pytest
from utils.api_client import ApiClient
from test_data import TestUserData

@allure.suite("API тесты для регистрации и авторизации")
class TestRegistrationLogin:
    @allure.title("Параметризованный тест невалидной регистрации") # По документации ожидается одно, по факту приходит другой код, баг.
    @pytest.mark.parametrize("invalid_data", TestUserData.invalid_registration_data())
    def test_invalid_registration(self, invalid_data):
        response = ApiClient.register_user(invalid_data)
        assert response.status_code == 400

    @allure.title("Создание дубликата пользователя")
    def test_create_duplicate_user(self, test_user):
        response = ApiClient.register_user({
            "email": test_user["email"],
            "password": "NewPass123",
            "name": "Duplicate User"
        })
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title("Авторизация с неверными данными")
    def test_login_invalid_credentials(self):
        response = ApiClient.login_user({
            "email": "invalid@user.com",
            "password": "WrongPass123"
        })
        assert response.status_code == 401