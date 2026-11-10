import math
def lookup_drink_code(code_string):
    menu_prices = {
        "LAT": 4.50,
        "CAP": 4.00,
        "ESP": 3.00,
        "AME": 3.50,
        "MOC": 5.00
    }

    if not isinstance(code_string, str) or not code_string.strip():
        return None

    code_prefix = code_string.strip().upper()[:3]

    return menu_prices.get(code_prefix)

def calculate_average_shot_cost(pricing_csv):
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        return None

    try:
        prices = [float(p.strip()) for p in pricing_csv.split(',')]

        if not prices:
            return None

        if any(not math.isfinite(p) or p < 0 for p in prices):
            return None

        return sum(prices) / len(prices)

    except ValueError:
        return None

def parse_order_modifiers(order_spec):
    if not isinstance(order_spec, str) or not order_spec.strip():
        return {}

    modifier_dict = {}
    items = order_spec.split(';')

    for item in items:
        if ':' not in item:
            return {}

        key, value = item.split(':', 1)
        key = key.strip()
        value = value.strip()

        if not key or not value:
            return {}

        if key in modifier_dict:
            return {}

        modifier_dict[key] = value

    return modifier_dict

def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)

if __name__ == "__main__":
    main()