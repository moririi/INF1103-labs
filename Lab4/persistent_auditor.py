MAX_CAPACITY = 500


def get_valid_input():
    failed_attempts = 0

    while True:
        stock = input("Enter stock quantity or 'quit': ").strip().lower()

        if stock == "quit":
            return "quit", failed_attempts

        if stock.startswith("-") and stock[1:].isdigit():
            print("Negative numbers are not allowed.")
            failed_attempts += 1
            continue

        if not stock.isdigit():
            print("Invalid input. Please enter a whole number.")
            failed_attempts += 1
            continue

        return int(stock), failed_attempts


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, total_deliveries, failed_attempts, history):
    print("\n--- Final Report ---")
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", total_deliveries)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Transaction history:", history)


def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            total = int(file.readline().strip())
            history = []

            for line in file:
                history.append(int(line.strip()))

            return total, history
    except FileNotFoundError:
        return 0, []


def save_inventory(total, history):
    with open("inventory.txt", "w") as file:
        file.write(f"{total}\n")

        for amount in history:
            file.write(f"{amount}\n")


# Load saved data before accepting new deliveries
inventory, transaction_history = load_inventory()
deliveries_processed = len(transaction_history)
failed_entries = 0

while True:
    remaining_capacity = MAX_CAPACITY - inventory
    print("\nRemaining capacity:", remaining_capacity, "units")

    if inventory == MAX_CAPACITY:
        print("Maximum inventory capacity reached.")
        break

    stock, new_failed_attempts = get_valid_input()
    failed_entries += new_failed_attempts

    if stock == "quit":
        break

    proposed_total = process_delivery(inventory, stock)

    if proposed_total > MAX_CAPACITY:
        print("Delivery rejected.")
        print("You can only add up to", remaining_capacity, "more units.")
        failed_entries += 1
        continue

    inventory = proposed_total
    transaction_history.append(stock)
    deliveries_processed += 1

    tax = calculate_tax(stock)
    print("Stock added successfully.")
    print("Delivery tax:", f"${tax:.2f}")
    print("Current inventory:", inventory, "units")

# Both 'quit' and reaching capacity lead here
save_inventory(inventory, transaction_history)
generate_report(
    inventory,
    deliveries_processed,
    failed_entries,
    transaction_history,
)