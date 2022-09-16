class Credential:

    username = ''
    password = ''

    def __init__(self, username=None, password=None) -> None:
        self.username = username
        self.password = password


    def get_password(self) -> str:
        return self.password

    def get_username(self) -> str:
        return self.username