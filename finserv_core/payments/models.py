from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Payment:
    id: str
    from_account: str
    to_account: str
    amount: Decimal
    currency: str
    status: PaymentStatus = PaymentStatus.PENDING