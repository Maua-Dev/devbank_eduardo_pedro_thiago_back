import pytest
from fastapi import HTTPException
from src.app.repo.user_repository_mock import UserRepositoryMock
# Importe suas funções aqui
from src.app.main import update_deposit, update_withdraw

class Test_User_Operations:
    def setup_method(self):
        # Reinicia o repositório antes de cada teste
        self.repo = UserRepositoryMock()

    def test_deposit_logic(self):
        body = {"100": 1} # 100 reais
        response = update_deposit(request=body)
        assert response["value"] == 100.0
        assert response["type"] == "deposit"

    def test_withdraw_insufficient_funds(self):
        # Tenta sacar mais do que o saldo inicial de 1000
        body = {"1000": 5} # 5000 reais
        with pytest.raises(HTTPException) as err:
            update_withdraw(request=body)
        assert err.value.status_code == 400