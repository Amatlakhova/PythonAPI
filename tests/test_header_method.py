import requests
from lib.base_case import BaseCase

class TestHeaderMethod(BaseCase):

    def test_header_method(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        actual_header_value = self.get_header(response, "x-secret-homework-header")
        print(actual_header_value)

        expected_header_value = "Some secret value"

        assert actual_header_value == expected_header_value, f"Expected header value is not equal to actual header value. Actual header value is '{actual_header_value}'"
