import pytest
from src.app.repo.user_repository_mock import UserRepositoryMock
from src.app.entities.user import User

class Test_UserRepositoryMock:

    def test_get_user_account(self):
        """Testa se o repositório consegue buscar o usuário padrão perfeitamente"""
        repo = UserRepositoryMock()
        user = repo.get_user_account()

        assert user is not None
        assert user.name == "Eduardo"
        assert user.agency == "0000"
        assert user.current_balance == 1000.0

    def test_update_balance(self):
        """Testa se a função de atualizar o saldo na memória está funcionando"""
        repo = UserRepositoryMock()
        
        # Atualiza o saldo para 500
        updated_user = repo.update_balance(500.0)
        
        assert updated_user is not None
        assert updated_user.current_balance == 500.0
        
        # Garante que ao buscar de novo, o saldo continua atualizado
        user_check = repo.get_user_account()
        assert user_check.current_balance == 500.0