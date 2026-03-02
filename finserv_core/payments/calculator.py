def calculate_fee(amount, percentage):
    # Bug: no validation, and incorrect rounding
    fee = amount * percentage
    return round(fee, 2)


def apply_discount(amount, discount):
    # Bug: discount can exceed 100%
    return amount - (amount * discount)
