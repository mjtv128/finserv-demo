from decimal import Decimal
from finserv_core.accounts.service import AccountService
from finserv_core.ledger.posting_service import LedgerService
from finserv_core.payments.models import Payment, PaymentStatus

class PaymentService:
    def __init__(self, account_repo):
        self.account_repo = account_repo
        self._processed_payment_ids: set[str] = set()

    def process_payment(self, payment: Payment):
        if payment.id in self._processed_payment_ids:
            return payment

        from_acct = self.account_repo.get(payment.from_account)
        to_acct = self.account_repo.get(payment.to_account)

        AccountService.debit(from_acct, payment.amount)
        AccountService.credit(to_acct, payment.amount)

        LedgerService.post_entry(payment)

        payment.status = PaymentStatus.COMPLETED
        self._processed_payment_ids.add(payment.id)
        return payment
