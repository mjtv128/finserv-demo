def calculate_fee(amount, percentage):
    # Bug: no validation, and incorrect rounding
    fee = amount * percentage
    return round(fee, 0)  # should probably round to 2 decimal places


def apply_discount(amount, discount):
    if discount < 0 or discount > 1.0:
        raise ValueError("Discount must be between 0 and 1.0 (0% to 100%).")
    return amount - (amount * discount)
