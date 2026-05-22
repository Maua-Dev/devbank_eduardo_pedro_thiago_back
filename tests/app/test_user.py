import pytest
from src.app.entities.user import User

class TestUser:
    def test_deposit_success(self):
        user = User(name="Teste", agency="0000", account="12345-6", current_balance=100.0)
        result = user.deposit(50.0)
        assert user.current_balance == 150.0
        assert result["current_balance"] == 150.0

    def test_withdraw_success(self):
        user = User(name="Teste", agency="0000", account="12345-6", current_balance=100.0)
        result = user.withdraw(40.0)
        assert user.current_balance == 60.0
        assert result["current_balance"] == 60.0

    def test_withdraw_insufficient_funds(self):
        user = User(name="Teste", agency="0000", account="12345-6", current_balance=100.0)
        result = user.withdraw(150.0)
        assert user.current_balance == 100.0
        assert result["current_balance"] == 100.0