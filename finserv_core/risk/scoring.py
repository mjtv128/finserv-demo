from decimal import Decimal

class RiskScorer:
    @staticmethod
    def score(amount: Decimal) -> int:
        if amount > Decimal("10000"):
            return 80
        return 10