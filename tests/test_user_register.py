import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Registration tests")
class TestUserRegister(BaseCase):
    @allure.description("This test creates user successfully")
    @allure.tag("Positive Test Case")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.suite("Smoke Test")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test checks that it is impossible to create user with existing email")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.suite("Smoke Test")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("This test checks that it is impossible to create user with invalid email")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.suite("Smoke Test")
    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"


    keys = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    @allure.description("This test checks that it is impossible to create user with missing field")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.suite("Regression")
    @pytest.mark.parametrize('key', keys)
    def test_create_user_with_missing_field(self, key):
        data = self.prepare_invalid_data(key)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {key}", f"Unexpected response content {response.content}"

    @allure.description("This test checks that it is impossible to create user with a short username")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.MINOR)
    @allure.suite("Regression")
    def test_create_user_with_short_name(self):
        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'a',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    @allure.description("This test checks that it is impossible to create user with a too long username")
    @allure.tag("Negative Test Case")
    @allure.severity(allure.severity_level.MINOR)
    @allure.suite("Regression")
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'a' * 251

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content {response.content}"
