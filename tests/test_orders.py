import allure
from utils.api_client import ApiClient

@allure.suite("API тесты заказов")
class TestOrders:
    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_authenticated(self, test_user, valid_ingredients):
        response = ApiClient.create_order(
            headers={"Authorization": test_user["accessToken"]},
            ingredients=valid_ingredients[:2]
        )
        assert response.status_code == 200