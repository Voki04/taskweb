class UserModel:
    def __init__(self):
        self.users = {
            "admin": "password"
        }

    def validate_user(self, username, password):
        return self.users.get(username) == password
