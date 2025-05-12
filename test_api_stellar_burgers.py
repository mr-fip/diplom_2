import pytest
import allure
import requests
import uuid

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@pytest.fixture
def unique_email():
    return f"user_{uuid.uuid4().hex}@example.com"

@pytest.fixture
def test_user(unique_email):
    user_data = {
        "email": unique_email,
        "password": "SecurePass123!",
        "name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    assert response.status_code == 200
    return {
        **user_data,
        "accessToken": response.json()["accessToken"]
    }

@allure.suite("API тесты для Stellar Burgers")
class TestUserRegistration:
    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешной регистрации нового пользователя")
    def test_create_unique_user(self, unique_email):
        data = {
            "email": unique_email,
            "password": "Password123",
            "name": "Unique User"
        }
        with allure.step("Отправка запроса на регистрацию"):
            response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "accessToken" in response.json()

    @allure.title("Попытка создания дубликата пользователя")
    @allure.description("Проверка обработки попытки регистрации уже существующего пользователя")
    def test_create_duplicate_user(self, test_user):
        data = {
            "email": test_user["email"],
            "password": "NewPass123",
            "name": "Duplicate User"
        }
        with allure.step("Отправка запроса на регистрацию с существующим email"):
            response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 403
            assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Проверка обработки запроса с отсутствующим обязательным полем 'name'")
    def test_create_user_missing_field(self):
        data = {
            "email": "missing@field.com",
            "password": "Pass123"
        }
        with allure.step("Отправка запроса на регистрацию без поля name"):
            response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 403
            assert "required fields" in response.json()["message"]

@allure.suite("API тесты для авторизации")
class TestUserLogin:
    @allure.title("Успешная авторизация пользователя")
    def test_login_valid_user(self, test_user):
        with allure.step("Отправка запроса на авторизацию с валидными данными"):
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": test_user["email"],
                "password": test_user["password"]
            })
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "accessToken" in response.json()

    @allure.title("Авторизация с неверными учетными данными")
    def test_login_invalid_credentials(self):
        with allure.step("Отправка запроса на авторизацию с неверными данными"):
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": "invalid@user.com",
                "password": "WrongPass123"
            })
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 401
            assert "incorrect" in response.json()["message"]

@allure.suite("API тесты для работы с профилем пользователя")
class TestUserProfile:
    @allure.title("Обновление данных пользователя с авторизацией")
    def test_update_user_with_auth(self, test_user):
        headers = {"Authorization": test_user["accessToken"]}
        new_data = {"name": "Updated Name"}
        
        with allure.step("Отправка запроса на обновление данных с авторизацией"):
            response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json=new_data)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert response.json()["user"]["name"] == "Updated Name"

    @allure.title("Обновление данных пользователя без авторизации")
    def test_update_user_without_auth(self):
        with allure.step("Отправка запроса на обновление данных без авторизации"):
            response = requests.patch(f"{BASE_URL}/auth/user", json={"email": "new@email.com"})
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 401
            assert "authorised" in response.json()["message"]

@allure.suite("API тесты для работы с заказами")
class TestOrders:
    @pytest.fixture
    def valid_ingredients(self):
        with allure.step("Получение списка доступных ингредиентов"):
            response = requests.get(f"{BASE_URL}/ingredients")
            return [ingredient["_id"] for ingredient in response.json()["data"]]

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_authenticated(self, test_user, valid_ingredients):
        headers = {"Authorization": test_user["accessToken"]}
        
        with allure.step("Отправка запроса на создание заказа с авторизацией"):
            response = requests.post(f"{BASE_URL}/orders", headers=headers, json={
                "ingredients": valid_ingredients[:2]
            })
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    @allure.description("Сервер должен вернуть статус-код 401 по API-документации")
    def test_create_order_unauthenticated(self, valid_ingredients):
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json={
                "ingredients": valid_ingredients[:1]
            })
        
        with allure.step("Проверка ответа (ожидается 401, но приложение возвращает 200 - это баг)"):
            assert response.status_code == 401

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, test_user):
        headers = {"Authorization": test_user["accessToken"]}
        
        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = requests.post(f"{BASE_URL}/orders", headers=headers, json={"ingredients": []})
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert "must be provided" in response.json()["message"]

    @allure.title("Создание заказа с невалидным хешем ингредиента")
    def test_create_order_invalid_hash(self, test_user):
        headers = {"Authorization": test_user["accessToken"]}
        
        with allure.step("Отправка запроса на создание заказа с невалидным хешем ингредиента"):
            response = requests.post(f"{BASE_URL}/orders", headers=headers, json={
                "ingredients": ["invalid_hash_123"]
            })
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 500

@allure.suite("API тесты для получения заказов")
class TestUserOrders:
    @allure.title("Получение списка заказов авторизованного пользователя")
    def test_get_orders_authenticated(self, test_user):
        headers = {"Authorization": test_user["accessToken"]}
        
        with allure.step("Отправка запроса на получение заказов с авторизацией"):
            response = requests.get(f"{BASE_URL}/orders", headers=headers)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "orders" in response.json()

    @allure.title("Получение списка заказов без авторизации")
    def test_get_orders_unauthenticated(self):
        with allure.step("Отправка запроса на получение заказов без авторизации"):
            response = requests.get(f"{BASE_URL}/orders")
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 401