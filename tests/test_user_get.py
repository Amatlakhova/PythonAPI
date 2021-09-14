import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Get data tests")
class TestUserGet(BaseCase):
    @allure.description("This test checks that it is impossible to get data of not authorized user, except from firstname")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.suite("Regression")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test checks that it is possible to get data of authorized user")
    @allure.tag("Positive Test Case")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.suite("Regression")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
            )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks that it is impossible to get user's data being logged in as other user")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.suite("Regression")
    def test_hack_user_data(self):
        # Register the hacker
        hacker = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=hacker)
        Assertions.assert_code_status(response, 200)

        # Auth the hacker
        data = {
            'email': hacker['email'],
            'password': hacker['password']
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Try to get data of other user being logged in as the hacker
        response2 = MyRequests.get(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
            )
        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response2, expected_fields)

