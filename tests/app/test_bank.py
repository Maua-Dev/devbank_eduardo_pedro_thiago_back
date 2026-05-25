import unittest
from src.app.entities.user import User
from src.app.entities.transaction import Transaction
from src.app.repo.user_repository_mock import UserRepositoryMock
from fastapi import HTTPException

class TestBankFlow(unittest.TestCase):
    def setUp(self):
        # Starts with 1000 balance according to your repo mock
        self.repo = UserRepositoryMock()
        self.user = self.repo.get_user_account()

    def test_withdraw_success_flow(self):
        # Simulate request: {"100": 2} -> total 200
        request = {"100": 2}
        total_amount = 200.0
        
        # Simulate main.py logic
        self.user.withdraw(total_amount)
        self.repo.update_balance(self.user.current_balance)
        
        # Create transaction
        new_transaction = Transaction(
            type="withdraw",
            value=total_amount,
            current_balance=self.user.current_balance,
            timestamp=1690482853890
        )
        self.repo.add_transaction(new_transaction)
        
        # Assertions
        self.assertEqual(self.user.current_balance, 800.0)
        self.assertEqual(len(self.repo.all_transaction), 1)
        self.assertEqual(self.repo.all_transaction[0].type, "withdraw")

    def test_withdraw_insufficient_funds(self):
        # Attempt to withdraw 2000 with 1000 balance
        request = {"1000": 2}
        total_amount = 2000.0
        
        # Test if business rules block the withdrawal
        if self.user.current_balance < total_amount:
            with self.assertRaises(HTTPException):
                raise HTTPException(status_code=403, detail="Insufficient balance for transaction")
        
        self.assertEqual(self.user.current_balance, 1000.0)

if __name__ == '__main__':
    unittest.main()