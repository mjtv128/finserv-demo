from payments.calculator import calculate_fee, apply_discount

def test_calculate_fee():
    assert calculate_fee(100, 0.05) == 5.00

def test_apply_discount():
    assert apply_discount(100, 0.10) == 90