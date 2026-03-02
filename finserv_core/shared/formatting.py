def format_currency(amount):
    # Bug: doesn't handle None
    return "$" + str(round(amount, 2))