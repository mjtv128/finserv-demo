from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Account:
    id: str
    owner: str
    balance: Decimal
    currency: str