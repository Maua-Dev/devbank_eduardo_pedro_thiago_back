from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from .environments import Environments

from .errors.entity_errors import ParamNotValidated

from .enums.item_type_enum import ItemTypeEnum

from .entities.item import Item

from .entities.user import User

from .repo.user_repository_mock import UserRepositoryMock

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = Environments.get_item_repo()()
user_repo = UserRepositoryMock()

# a baixo estão as rotas da api
# elas interagem com os métodos de repositório. por exemplo a rota create item chama, não exclusivamente,
# o método repo.create_item() para criar o item no nosso repositório

@app.get("/items/get_all_items")
def get_all_items():
    items = repo.get_all_items()
    return {
        "items": [item.to_dict() for item in items]
    }

@app.get("/items/{item_id}")
def get_item(item_id: str):
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    return {
        "item_id": item_id,
        "item": item.to_dict()    
    }

@app.get("/")
def get_user_dashboard():
    user = user_repo.get_user_account()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    
    return {
        "name": user.name,
        "agency": user.agency,
        "account": user.account,
        "current_balance": user.current_balance
    }

@app.post("/items/create_item", status_code=201)
def create_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    # por exemplo, dentro da rota create item, chamamos um get_item para checar se o item ja existe
    # em nosso repositorio
    
    item = repo.get_item(item_id)
    if item is not None:
        raise HTTPException(status_code=409, detail="Item already exists")
    
    name = request.get("name")
    price = request.get("price")
    item_type = request.get("item_type")
    if item_type is None:
        raise HTTPException(status_code=400, detail="Item type is required")
    if type(item_type) != str:
        raise HTTPException(status_code=400, detail="Item type must be a string")
    if item_type not in [possible_type.value for possible_type in ItemTypeEnum]:
        raise HTTPException(status_code=400, detail="Item type is not a valid one")
    
    admin_permission = request.get("admin_permission")
    
    try:
        item = Item(
            item_id=item_id,
            name=name,
            price=price,
            item_type=ItemTypeEnum[item_type], 
            # bate a string que veio na request com todos os .values dentro do enum ItemTypeEnum.
            # ou seja, se vier uma string TOY ele vai converter para ItemTypeEnum.TOY
            admin_permission=admin_permission,
        )
    except ParamNotValidated as err:
        raise HTTPException(status_code=400, detail=err.message)
    
    item_response = repo.create_item(item)
    return {
        "item_id": item_id,
        "item": item_response.to_dict()    
    }
    
@app.delete("/items/delete_item")
def delete_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")

    item_deleted = repo.delete_item(item_id)
    
    return {
        "item_id": item_id,
        "item": item_deleted.to_dict()    
    }
    
@app.put("/items/update_item")
def update_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")

    name = request.get("name")
    price = request.get("price")
    admin_permission = request.get("admin_permission")

    item_type_value = request.get("item_type")
    if item_type_value != None:
        if type(item_type_value) != str:
            raise HTTPException(status_code=400, detail="Item type must be a string")
        if item_type_value not in [possible_type.value for possible_type in ItemTypeEnum]:
            raise HTTPException(status_code=400, detail="Item type is not a valid one")
        item_type = ItemTypeEnum[item_type_value]
    else:
        item_type = None
        
    item_updated = repo.update_item(item_id, name, price, item_type, admin_permission)
    
    return {
        "item_id": item_id,
        "item": item_updated.to_dict()    
    }
    
@app.post("/withdraw")  
def withdraw(request: dict):
    user = user_repo.get_user_account()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    
    total_amount = 0
    for nota, quantidade in request.items():
        total_amount += float(nota) * int(quantidade)
    
    old_balance = user.current_balance
    
    result = user.withdraw(total_amount)
    
    if user.current_balance == old_balance and total_amount > 0:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar o saque")
    
    user_repo.update_balance(user.current_balance)
        
    return result


@app.post("/deposit")  
def deposit(request: dict):
    user = user_repo.get_user_account()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    
    total_amount = 0
    for nota, quantidade in request.items():
        total_amount += float(nota) * int(quantidade)
    
    result = user.deposit(total_amount)
    
    user_repo.update_balance(user.current_balance)
        
    return result

handler = Mangum(app, lifespan="off")
