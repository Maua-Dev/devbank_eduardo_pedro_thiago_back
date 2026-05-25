from typing import List, Optional
from ..entities.user import User

class UserRepositoryMock:
    def __init__(self):
        self.user = User(
            name = "Eduardo",
            agency = "0000",
            account = "12345-6",
            current_balance = 1000.0
        )

        self.all_transaction = []
        
        self.users: List[User] = [self.user]

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
    
    def add_transaction(self, transaction):
        self.all_transaction.append(transaction)                                                            