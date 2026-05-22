import re
from typing import Tuple
from ..errors.entity_errors import ParamNotValidated

class User():
    """
    Entity representing a DevBank User/Customer.
    
    Responsible for carrying registration data, current balance, and enforcing
    validation rules for bank agency and account formats.
    
    """
    name: str
    agency: str
    account: str
    current_balance: float

    def __init__(self, name: str = None, agency: str = None, account: str = None, current_balance: float = None):
        """
        Instantiates a new DevBank user and triggers format validations.
        
        Raises:
            ParamNotValidated: If any of the provided parameters are invalid.
        """

        validation_name = self.validate_name(name)

        if validation_name[0] is False:
            raise ParamNotValidated("name", validation_name[1])
        
        # No error: Parameter is valid, safe to initialize the attribute
        self.name = name 

        validation_agency = self.validate_agency(agency)
        if validation_agency[0] is False:
            raise ParamNotValidated("agency", validation_agency[1])
        
        # No error: Parameter is valid, safe to initialize the attribute
        self.agency = agency

        validation_account = self.validate_account(account)
        if validation_account[0] is False:
            raise ParamNotValidated("account", validation_account[1])
        
        # No error: Parameter is valid, safe to initialize the attribute
        self.account = account

        validation_current_balance = self.validate_current_balance(current_balance)
        if validation_current_balance[0] is False:
            raise ParamNotValidated("current_balance", validation_current_balance[1])
        
        # No error: Parameter is valid, safe to initialize the attribute
        self.current_balance = current_balance        
        
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Ensures the name is a non-null string with at least 3 characters."""
        
        if name is None:
            return (False, "Name is required")
        if type(name) != str:
            return (False, "Name must be a string")
        if len(name) < 3:
            return (False, "Name must be at least 3 characters long")
        
        return (True, "") # No errors
    
    @staticmethod
    def validate_agency(agency: str) -> Tuple[bool, str]:
        """Validates that the agency contains exactly 4 numeric digits (e.g., '0000')."""

        if agency is None:
            return (False, "Agency is required")
        if type(agency) != str:
            return (False, "Agency must be a string")
        
        # Regex breakdown: ^ (start), \d{4} (exactly 4 digits), $ (end)
        if not re.match(r"^\d{4}$", agency): 
            return (False, "Agency must contain exactly 4 numeric digits")
        
        return (True, "") # No errors
    
    @staticmethod
    def validate_account(account: str) -> Tuple[bool, str]:
        """Validates that the account follows the required 6-digit pattern: XXXXX-X (e.g., '12345-6')."""

        if account is None:
            return (False, "Account is required")
        if type(account) != str:
            return (False, "Account must be a string")
        
        # Regex breakdown: ^ (start), \d{5} (exactly 5 digits) and \d{1} (exactly 1 digit), - is '-' (char -), $ (end)
        if re.match(r"^\d{5}-\d{1}$", account):
            return (False, "Account must follow the XXXXX-X format")
        
        return (True, "") # No errors
    
    @staticmethod
    def validate_current_balance(current_balance: float) -> Tuple[bool, str]:
        """Ensures the initial balance is a non-null positive number."""

        if current_balance is None:
            return (False, "Current Balance is required")
        if type(current_balance) not in [int, float]:
            return (False, "Current balance must be a number")
        if current_balance < 0:
            return (False, "Current balance cannot be negative")        
        
        return (True, "") # No errors
    
    def to_dict(self):
        return {
            "name": self.name,
            "agency": self.agency,
            "account": self.account,
            "current_balance": self.current_balance
        }
    
    def deposit(self, deposit_amount: float) -> dict:
        """
        Deposit logic:
        - Is the received amount greater than or equal to 0?
        - If true, do current_balance += deposit_amount
        """
        if deposit_amount >= 0:
            self.current_balance += deposit_amount
            
        return self.to_dict()

    def withdraw(self, withdrawal_amount: float) -> dict:
        """
        Withdrawal logic:
        - Is the received amount greater than or equal to 0?
        - If current_balance > withdrawal_amount, do current_balance -= withdrawal_amount
        """
        if withdrawal_amount >= 0:
            if self.current_balance > withdrawal_amount:
                self.current_balance -= withdrawal_amount
                
        return self.to_dict()
    
    def __eq__(self, other):
        """Defines the rules for comparing two User instances using the '==' operator."""

        return (
            self.name == other.name and
            self.agency == other.agency and
            self.account == other.account and
            self.current_balance == other.current_balance
        )
    
    def __repr__(self):
        """Returns a clear and readable string representation of the User object for debugging."""

        return f"""
            User:
            name = {self.name},
            agency = {self.agency},
            account = {self.account},
            current_balance = {self.current_balance}
        """