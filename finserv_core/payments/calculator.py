def calculate_fee(amount, percentage):
    # Bug: no validation, and incorrect rounding
    fee = amount * percentage
    return round(fee, 0)  # should probably round to 2 decimal places


def apply_discount(amount, discount):
    # Bug: discount can exceed 100%
    return amount - (amount * discount)