class TestUserData:
    VALID_PASSWORD = "SecurePass123!"
    INVALID_PASSWORDS = ["short", "noDigits!", "ALL_CAPS_NODIGITS"]
    BASE_NAME = "Test User"
    
    @staticmethod
    def invalid_registration_data():
        return [
            {"password": "pass", "name": "Missing Email"},
            {"email": "missing@password.com", "name": "Missing Password"},
            {"email": "missing@name.com", "password": "pass123"}
        ]