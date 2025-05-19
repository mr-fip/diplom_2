import allure
from utils.api_client import ApiClient

@allure.suite("API тесты профиля пользователя")
class TestUserProfile:
    @allure.title("Обновление профиля с авторизацией")
    def test_update_user_with_auth(self, test_user):
        response = ApiClient.update_user(
            headers={"Authorization": test_user["accessToken"]},
            data={"name": "Updated Name"}
        )
        assert response.status_code == 200
        assert response.json()["user"]["name"] == "Updated Name"