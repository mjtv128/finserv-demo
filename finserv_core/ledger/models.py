from dataclasses import dataclass
from decimal import Decimal

@dataclass
class LedgerEntry:
    payment_id: str
    debit_account: str
    credit_account: str
    amount: Decimal