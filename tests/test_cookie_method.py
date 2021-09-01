import requests
from lib.base_case import BaseCase

class TestCookieMethod(BaseCase):

    def test_cookie_method(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        actual_cookie_value = self.get_cookie(response, "HomeWork")
        print(actual_cookie_value)

        expected_cookie_value = "hw_value"

        assert actual_cookie_value == expected_cookie_value, f"Expected cookie value is not equal to actual cookie value. Actual cookie value is '{actual_cookie_value}'"
