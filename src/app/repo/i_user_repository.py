from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    def get_user_account(self) -> Optional[User]:
        pass

    @abstractmethod
    def update_balance(self, new_balance: float) -> Optional[User]:
        pass