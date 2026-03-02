from decimal import Decimal
from finserv_core.accounts.service import AccountService
from finserv_core.ledger.posting_service import LedgerService
from finserv_core.payments.models import Payment, PaymentStatus
from finserv_core.shared.exceptions import CurrencyMismatchError

class PaymentService:
    def __init__(self, account_repo):
        self.account_repo = account_repo

    def process_payment(self, payment: Payment):
        from_acct = self.account_repo.get(payment.from_account)
        to_acct = self.account_repo.get(payment.to_account)

        if from_acct.currency != to_acct.currency:
            raise CurrencyMismatchError(
                f"Currency mismatch: source account is {from_acct.currency} "
                f"but destination account is {to_acct.currency}"
            )

        if payment.currency != from_acct.currency:
            raise CurrencyMismatchError(
                f"Currency mismatch: payment currency is {payment.currency} "
                f"but account currency is {from_acct.currency}"
            )

        AccountService.debit(from_acct, payment.amount)
        AccountService.credit(to_acct, payment.amount)

        LedgerService.post_entry(payment)

        payment.status = PaymentStatus.COMPLETED
        return payment
