from decimal import Decimal
from finserv_core.accounts.service import AccountService
from finserv_core.ledger.posting_service import LedgerService
from finserv_core.payments.models import Payment, PaymentStatus

class PaymentService:
    def __init__(self, account_repo):
        self.account_repo = account_repo

    def process_payment(self, payment: Payment):
        from_acct = self.account_repo.get(payment.from_account)
        to_acct = self.account_repo.get(payment.to_account)

        # Snapshot balances before mutation so we can roll back on failure
        original_from_balance = from_acct.balance
        original_to_balance = to_acct.balance

        try:
            AccountService.debit(from_acct, payment.amount)
            AccountService.credit(to_acct, payment.amount)
            LedgerService.post_entry(payment)
        except Exception:
            # Roll back balances to their pre-transaction state
            from_acct.balance = original_from_balance
            to_acct.balance = original_to_balance
            payment.status = PaymentStatus.FAILED
            raise

        payment.status = PaymentStatus.COMPLETED
        return payment
