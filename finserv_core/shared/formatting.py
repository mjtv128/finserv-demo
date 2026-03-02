def format_currency(amount):
    if amount is None:
        return None
    return "$" + str(round(amount, 2))
