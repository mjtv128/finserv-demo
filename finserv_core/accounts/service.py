from decimal import Decimal
from .models import Account
from finserv_core.shared.exceptions import InsufficientFundsError

class AccountService:
    @staticmethod
    def debit(account: Account, amount: Decimal):
        if account.balance < amount:
            raise InsufficientFundsError("Insufficient funds")
        account.balance -= amount

    @staticmethod
    def credit(account: Account, amount: Decimal):
        account.balance += amount