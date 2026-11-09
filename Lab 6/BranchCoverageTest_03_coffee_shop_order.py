
import pytest

from coffee_shop_order import (
    process_order_batch,
    check_espresso_machine,
)


# 1. Input validation branches
def test_valid_and_invalid_orders():
    with pytest.raises(ValueError):
        process_order_batch("invalid", 0.1)

    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


# 2. Payment branches
def test_paid_and_unpaid_orders():
    result = process_order_batch(
        [
            {"paid": True, "size": "medium"},
            {"paid": False, "size": "large"},
        ],
        0,
    )
    assert result == {"total": 4.5, "status": "COMPLETED"}


# 3. Coffee size branches
def test_all_coffee_sizes():
    result = process_order_batch(
        [
            {"paid": True, "size": "small"},
            {"paid": True, "size": "medium"},
            {"paid": True, "size": "large"},
        ],
        0,
    )
    assert result == {"total": 13.5, "status": "COMPLETED"}


def test_invalid_coffee_size():
    result = process_order_batch(
        [{"paid": True, "size": "extra_large"}],
        0,
    )
    assert result == {"total": 0.0, "status": "NO_SALE"}


# 4. Customization cost branches
def test_negative_and_nonnegative_customization_cost():
    result = process_order_batch(
        [{
            "paid": True,
            "size": "medium",
            "customizations": [
                {"type": "standard", "cost": -1},
                {"type": "standard", "cost": 0.5},
            ],
        }],
        0,
    )
    assert result == {"total": 5.0, "status": "COMPLETED"}


# 5. Allergen handling branches
def test_strict_and_non_strict_allergy():
    result = process_order_batch(
        [
            {
                "paid": True,
                "size": "medium",
                "strict_allergy": False,
                "customizations": [{"type": "allergen_alert"}],
            },
            {
                "paid": True,
                "size": "small",
                "strict_allergy": True,
                "customizations": [{"type": "allergen_alert"}],
            },
        ],
        0,
    )
    assert result == {"total": 4.5, "status": "COMPLETED"}


# 6. Syrup cost branches
def test_syrup_cost_limit():
    result = process_order_batch(
        [
            {
                "paid": True,
                "size": "medium",
                "customizations": [{"type": "syrup", "cost": 1.5}],
            },
            {
                "paid": True,
                "size": "medium",
                "customizations": [{"type": "syrup", "cost": 2.0}],
            },
        ],
        0,
    )
    assert result == {"total": 12.0, "status": "COMPLETED"}


# 7. Membership branches
def test_member_and_nonmember():
    result = process_order_batch(
        [
            {"paid": True, "size": "medium", "is_member": True},
            {"paid": True, "size": "medium", "is_member": False},
        ],
        0,
    )
    assert result == {"total": 8.55, "status": "COMPLETED"}


# 8. Final status branches
def test_completed_status():
    result = process_order_batch(
        [{"paid": True, "size": "small"}],
        0.1,
    )
    assert result == {"total": 3.3, "status": "COMPLETED"}


def test_no_sale_status():
    result = process_order_batch([], 0)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_audit_rejected_status():
    orders = [
        {"paid": True, "size": "invalid"}
        for _ in range(5)
    ]
    result = process_order_batch(orders, 0)
    assert result == {"total": 0.0, "status": "AUDIT_REJECTED"}


# 9. Espresso machine branches
def test_no_temperature_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_normal_and_high_temperatures():
    assert check_espresso_machine(
        [[90.0, 98.0, 90.0]]
    ) == "OPTIMAL"


def test_consecutive_overheating():
    assert check_espresso_machine(
        [[98.0, 99.0]]
    ) == "SHUTDOWN"


def test_overheating_streak_reset():
    assert check_espresso_machine(
        [[98.0, 90.0, 98.0]]
    ) == "OPTIMAL"
