
import pytest

from coffee_shop_order import (
    process_order_batch,
    check_espresso_machine,
)


# 1. Input validation
def test_invalid_orders():
    with pytest.raises(ValueError):
        process_order_batch("invalid", 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


# 2. Coffee sizes and payment
def test_small_coffee():
    result = process_order_batch(
        [{"paid": True, "size": "small"}], 0
    )
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_large_coffee():
    result = process_order_batch(
        [{"paid": True, "size": "large"}], 0
    )
    assert result == {"total": 6.0, "status": "COMPLETED"}


def test_unpaid_order():
    result = process_order_batch(
        [{"paid": False, "size": "medium"}], 0
    )
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_invalid_coffee_size():
    result = process_order_batch(
        [{"paid": True, "size": "extra_large"}], 0
    )
    assert result == {"total": 0.0, "status": "NO_SALE"}


# 3. Customizations
def test_negative_customization_cost():
    result = process_order_batch(
        [{
            "paid": True,
            "size": "medium",
            "customizations": [{"type": "syrup", "cost": -1}]
        }],
        0,
    )
    assert result == {"total": 4.5, "status": "COMPLETED"}


def test_syrup_cost_within_limit():
    result = process_order_batch(
        [{
            "paid": True,
            "size": "medium",
            "customizations": [{"type": "syrup", "cost": 1}]
        }],
        0,
    )
    assert result["total"] == 5.5


def test_syrup_cost_above_limit():
    result = process_order_batch(
        [{
            "paid": True,
            "size": "medium",
            "customizations": [{"type": "syrup", "cost": 2}]
        }],
        0,
    )
    assert result["total"] == 6.0


def test_standard_customization():
    result = process_order_batch(
        [{
            "paid": True,
            "size": "medium",
            "customizations": [{"type": "standard", "cost": 0.5}]
        }],
        0,
    )
    assert result["total"] == 5.0


# 4. Allergy handling
def test_allergen_alert_non_strict():
    result = process_order_batch(
        [{
            "paid": True,
            "size": "medium",
            "strict_allergy": False,
            "customizations": [{"type": "allergen_alert"}]
        }],
        0,
    )
    assert result == {"total": 4.5, "status": "COMPLETED"}


def test_allergen_alert_strict():
    result = process_order_batch(
        [{
            "paid": True,
            "size": "medium",
            "strict_allergy": True,
            "customizations": [{"type": "allergen_alert"}]
        }],
        0,
    )
    assert result == {"total": 0.0, "status": "NO_SALE"}


# 5. Membership discount and tax
def test_member_discount():
    result = process_order_batch(
        [{"paid": True, "size": "medium", "is_member": True}], 0
    )
    assert result["total"] == 4.05


def test_tax_calculation():
    result = process_order_batch(
        [{"paid": True, "size": "medium"}], 0.1
    )
    assert result["total"] == 4.95


# 6. Rejection threshold
def test_audit_rejected():
    orders = [
        {
            "paid": True,
            "size": "invalid",
        }
        for _ in range(5)
    ]
    result = process_order_batch(orders, 0)
    assert result == {"total": 0.0, "status": "AUDIT_REJECTED"}


# 7. Espresso machine monitoring
def test_no_temperature_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_normal_temperature():
    assert check_espresso_machine([[90.0, 94.0]]) == "OPTIMAL"


def test_single_overheat():
    assert check_espresso_machine([[98.0, 90.0]]) == "OPTIMAL"


def test_consecutive_overheating():
    assert check_espresso_machine([[98.0, 99.0]]) == "SHUTDOWN"


def test_overheating_streak_reset():
    assert check_espresso_machine([[98.0, 90.0, 98.0]]) == "OPTIMAL"
