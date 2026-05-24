from typing import Dict
from src.app.errors.entity_errors import ParamNotValidated

class Transaction:
    def __init__(self, cash_input: Dict[str, int], transaction_type: str):
        self.cash_input = cash_input
        self.transaction_type = transaction_type
        self.validate_cash_input(cash_input)
        self.total_value = self.calculate_total_value(cash_input)

    @staticmethod
    def validate_cash_input(cash_input: Dict[str, int]):
        if not cash_input or len(cash_input) == 0:
            raise ParamNotValidated("cash_input", "É necessário inserir algum valor para a transação.")
        
        for note, quantity in cash_input.items():
            if not note.isdigit() or int(note) not in [2, 5, 10, 20, 50, 100, 200]:
                raise ParamNotValidated("cash_input", f"A cédula de R$ {note} não é válida.")
            if quantity <= 0:
                raise ParamNotValidated("cash_input", "A quantidade de notas deve ser maior que zero.")

    @staticmethod
    def calculate_total_value(cash_input: Dict[str, int]) -> float:
        total = 0.0
        for note, quantity in cash_input.items():
            total += float(note) * quantity
        return total

    def to_dict(self) -> Dict:
        return {"transaction_type": self.transaction_type, "value_processed": self.total_value,"cash_details": self.cash_input}