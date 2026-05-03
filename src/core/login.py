import json
import logging

from pathlib import Path
from ..utils.file_paths import USERS


class Login:
    def __init__(self, logger: logging.Logger, users_file: Path = USERS):
        self.logger = logger
        self.users_file = users_file
        self.users = {}
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.logger.warning("Users DataBase File not Found.")
            raise

    def add_users(self, user_id: str, password: str):
        if user_id in self.users:
            self.logger.warning(f"User {user_id.title()} Already Exists. [Log In Instead]")
            return
        self.users[user_id] = password
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def login_user(self, user_id: str, password: str):
        if user_id not in self.users:
            self.logger.warning(f"User {user_id.title()} does not Exist.")
            return False
        if self.users[user_id] == password:
            self.logger.info(f"User {user_id.title()} Logged in Successfully.")
            return True
        self.logger.warning(f"Failed Login Attempt for User {user_id.title()}.")
        return False

    def get_login_info(self):
        while True:
            login_info = input("Enter User ID: ").strip()
            if login_info:
                return login_info
            self.logger.warning(
                "Invalid. "
                "User ID or Password must be a Non-Empty String.\n"
                "Please Enter a Valid, Non-Empty String."
            )
