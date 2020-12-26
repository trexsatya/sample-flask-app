

class AuthException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(str)

    def __str__(self):
        return f"Auth Failure: {self.message}"
