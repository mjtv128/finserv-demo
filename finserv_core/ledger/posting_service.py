from finserv_core.ledger.models import LedgerEntry

class LedgerService:
    entries = []

    @classmethod
    def post_entry(cls, payment):
        entry = LedgerEntry(
            payment_id=payment.id,
            debit_account=payment.from_account,
            credit_account=payment.to_account,
            amount=payment.amount,
        )
        cls.entries.append(entry)