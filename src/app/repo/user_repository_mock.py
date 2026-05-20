from typing import List, Optional
from ..entities.user import User

class UserRepositoryMock:
    def __init__(self):
        user = User.__new__(User)
        user.name = "Eduardo"
        user.agency = "0000"
        user.account = "123456"
        user.current_balance = 1000.0
        
        self.users: List[User] = [user]

    def get_user_account(self) -> Optional[User]:
        if len(self.users) > 0:
            return self.users[0]
        return None

    def update_balance(self, new_balance: float) -> Optional[User]:
        user = self.get_user_account()
        if user:
            user.current_balance = new_balance
            return user
        return None