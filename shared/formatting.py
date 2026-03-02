def format_currency(amount):
    if amount is None:
        return "$0.00"
    return "$" + str(round(amount, 2))
