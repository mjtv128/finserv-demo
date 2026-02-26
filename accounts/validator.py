def validate_email(email):
    # Bug: no None check
    if "@" not in email:
        return False
    return True


def validate_age(age):
    # Bug: negative age allowed
    if age > 0:
        return True
    return False