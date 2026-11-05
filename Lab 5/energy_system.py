
"""
Energy Tariff Management System.

Records electricity meter readings, calculates bills, adjusts tariff
rates, detects consumption spikes, and stores meter data in JSON format.
"""

import json
from datetime import datetime

# Global meter data and tariff configuration
meters = {}

RATE_TIER_1 = 3.5
RATE_TIER_2 = 5.0
RATE_TIER_3 = 7.5

SPIKE_LIMIT = 500


def record_reading(meter_id, units, history=None):
    """Record a meter reading and update the total consumption."""
    if units < 0:
        raise ValueError("Meter reading cannot be negative.")

    if history is None:
        history = []

    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units

    return history


def compute_bill(meter_id, tier_rates):
    """Calculate the electricity bill using three consumption tiers."""
    if meter_id not in meters:
        raise ValueError(f"Unknown meter ID: {meter_id}")

    units = meters[meter_id]

    if units <= 100:
        return units * tier_rates[0]

    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]

    return (
        100 * tier_rates[0]
        + 200 * tier_rates[1]
        + (units - 300) * tier_rates[2]
    )


def raise_rates(percent, rates):
    """Return tariff rates after applying a percentage increase."""
    if percent < 0:
        raise ValueError("Rate increase percentage cannot be negative.")

    return [rate * (1 + percent / 100) for rate in rates]


def flag_spikes():
    """Return meter IDs whose consumption exceeds the spike limit."""
    return [
        meter_id
        for meter_id, units in meters.items()
        if units > SPIKE_LIMIT
    ]


def load_meter_data(file="meters.json"):
    """Load meter data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as meter_file:
            loaded_data = json.load(meter_file)

        if not isinstance(loaded_data, dict):
            raise ValueError("Meter data must be a JSON object.")

        meters.clear()
        meters.update(loaded_data)

    except FileNotFoundError:
        meters.clear()
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Unable to load meter data: {error}")
        meters.clear()


def save_meter_data(file="meters.json"):
    """Save the current meter data to a JSON file."""
    with open(file, "w", encoding="utf-8") as meter_file:
        json.dump(meters, meter_file, indent=4)


def main():
    """Run the energy tariff management demonstration."""
    reading_history = []

    record_reading("M-01", 120, reading_history)
    record_reading("M-02", 640, reading_history)

    try:
        record_reading("M-03", -50, reading_history)
    except ValueError as error:
        print(f"Reading rejected: {error}")

    print("Readings stored so far:", len(reading_history))

    rates = [RATE_TIER_1, RATE_TIER_2, RATE_TIER_3]
    rates = raise_rates(10, rates)

    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print("Spikes:", flag_spikes())

    adjustment = input(
        "Extra units for M-01 (Enter for 0): "
    ) or "0"

    try:
        extra_units = int(adjustment)
        record_reading("M-01", extra_units, reading_history)
    except ValueError as error:
        print(f"Invalid reading: {error}")

    save_meter_data()
    load_meter_data()

    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
