from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):

        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
            )

        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )


    def test_edit_not_auth_user(self):

        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # Edit
        new_name = "Changed Name"

        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
            )

        Assertions.assert_code_status(response2, 400)

    def test_edit_other_user_data(self):
        # Register user 1
        user1 = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=user1)
        user_id = self.get_json_value(response, "id")

        Assertions.assert_code_status(response, 200)

        # Register user 2
        user2 = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=user2)
        Assertions.assert_code_status(response1, 200)

        # Auth user 2
        data = {
            'email': user2['email'],
            'password': user2['password']
        }

        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Try to edit user 1
        new_email = "changed@email.com"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)


    def test_edit_user_email_to_invalid(self):
        # Register user
        user = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=user)
        user_id = self.get_json_value(response, "id")

        Assertions.assert_code_status(response, 200)

        # Auth user
        data = {
            'email': user['email'],
            'password': user['password']
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Try to edit user's email
        new_email = user['email'].replace('@', '')

        response2 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response2, 400)

    def test_edit_user_firstname_to_invalid(self):
        # Register user
        user = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=user)
        user_id = self.get_json_value(response, "id")

        Assertions.assert_code_status(response, 200)

        # Auth user
        data = {
            'email': user['email'],
            'password': user['password']
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Try to edit user's firstname
        new_firstname = "a"

        response2 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstname}
        )

        Assertions.assert_code_status(response2, 400)
