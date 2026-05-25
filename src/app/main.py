from time import time

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from mangum import Mangum

from .environments import Environments

from .errors.entity_errors import ParamNotValidated

from .enums.item_type_enum import ItemTypeEnum

from .entities.item import Item

from .entities.user import User

from .repo.user_repository_mock import UserRepositoryMock

from .entities.transaction import Transaction

app = FastAPI()

repo = Environments.get_item_repo()()
user_repo = UserRepositoryMock()

@app.get("/")
def get_user_dashboard():
    user = user_repo.get_user_account()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    
    return {
        "name": str(user.name),
        "agency": str(user.agency),
        "account": str(user.account),
        "current_balance": float(user.current_balance)
    }
    
@app.post("/withdraw")  
def update_withdraw(request: dict):
    user = user_repo.get_user_account()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    
    total_amount = 0
    for nota, quantidade in request.items():
        total_amount += float(nota) * int(quantidade)
    
    if user.current_balance < total_amount:
        raise HTTPException(status_code=400, detail="Insufficient balance to perform the withdrawal")
    
    user.withdraw(total_amount) # Process withdrawal on the User object

    user_repo.update_balance(user.current_balance) # Synchronize the new balance in the repository
    
    new_transaction = Transaction(
        type="withdraw",
        value=total_amount,
        current_balance=user.current_balance,
        timestamp=int(time() * 1000)
    )
    
    user_repo.add_transaction(new_transaction)
    
    return new_transaction.to_dict()

@app.post("/deposit")  
def update_deposit(request: dict):
    user = user_repo.get_user_account()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    
    total_amount = 0
    for nota, quantidade in request.items():
        total_amount += float(nota) * int(quantidade)
    
    user.deposit(total_amount) # Update user
    user_repo.update_balance(user.current_balance)
    
    # Register the deposit transaction
    new_transaction = Transaction(
        type="deposit",
        value=total_amount,
        current_balance=user.current_balance,
        timestamp=int(time() * 1000)
    )
    user_repo.add_transaction(new_transaction)
        
    return new_transaction.to_dict()


@app.get("/history")
def get_history():
    # Returns only the list present in the repo
    return {
        "all_transactions": [t.to_dict() for t in user_repo.all_transaction]
    }


handler = Mangum(app, lifespan="off")