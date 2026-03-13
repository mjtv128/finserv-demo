from decimal import Decimal
from finserv_core.accounts.models import Account
from finserv_core.infrastructure.repository import InMemoryAccountRepository
from finserv_core.payments.models import Payment, PaymentStatus
from finserv_core.payments.service import PaymentService

def test_payment_success():
    a1 = Account(id="A1", owner="Alice", balance=Decimal("1000"), currency="USD")
    a2 = Account(id="A2", owner="Bob", balance=Decimal("500"), currency="USD")

    repo = InMemoryAccountRepository([a1, a2])
    service = PaymentService(repo)

    payment = Payment(
        id="P1",
        from_account="A1",
        to_account="A2",
        amount=Decimal("100"),
        currency="USD"
    )

    result = service.process_payment(payment)

    assert a1.balance == Decimal("900")
    assert a2.balance == Decimal("600")
    assert result.status == PaymentStatus.COMPLETED
