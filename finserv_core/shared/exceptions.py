class FinservError(Exception):
    pass

class InsufficientFundsError(FinservError):
    pass

class CurrencyMismatchError(FinservError):
    pass
