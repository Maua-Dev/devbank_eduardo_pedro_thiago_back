class Transaction:
    def __init__(self, type: str, value: float, current_balance: float, timestamp: int):
        self.type = type
        self.value = value
        self.current_balance = current_balance
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "current_balance": self.current_balance,
            "timestamp": self.timestamp
        }