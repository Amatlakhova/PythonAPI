import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Deletion tests")
class TestUserDelete(BaseCase):
    @allure.description("This test tries to delete user by id, but not allowed")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.suite("Regression")
    def test_delete_user_by_id(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        response1 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response1, 400)

    @allure.description("This test successfully deletes user by id")
    @allure.tag("Positive Test Case")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.suite("Smoke Test")
    def test_delete_user_successfully(self):
        # Register user
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        user_id = self.get_json_value(response, "id")

        # Login
        login_data = {
            'email': data['email'],
            'password': data['password']
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Delete
        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 200)

        # Get
        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 404)

    @allure.description("This test checks that it is impossible to delete a user being logged in as other user")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.suite("Regression")
    def test_delete_other_user(self):
        # Register user 1
        user1 = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=user1)
        user_id = self.get_json_value(response, "id")

        Assertions.assert_code_status(response, 200)

        # Auth user 2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Try to delete user 1
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 400)