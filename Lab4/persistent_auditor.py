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
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, total_deliveries, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", total_deliveries)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            return int(file.readline().strip())
    except FileNotFoundError:
        return 0
    
# Main prog
inventory = load_inventory()
deliveries_processed = 0
failed_entries = 0

while True:
    remaining_capacity = 500 - inventory
    print("\nRemaining capacity:", remaining_capacity, "units")

    stock, new_failed_attempts = get_valid_input()
    failed_entries += new_failed_attempts
    # Continue to next iteration if user wants to quit
    if stock == "quit":
        break

    # Check if the new stock exceeds the maximum capacity
    proposed_total = process_delivery(inventory, stock)

    if proposed_total > 500:
        print("Delivery rejected.")
        print(
            "You can only add up to",
            remaining_capacity,
            "more units."
        )
        failed_entries += 1
        continue
    # If the new stock is valid, update the inventory and process the delivery
    inventory = proposed_total
    deliveries_processed += 1

    tax = calculate_tax(stock)

    print("Stock added successfully.")
    print("Delivery tax:", f"${tax:.2f}")
    print("Current inventory:", inventory, "units")

    # Automatically finish when max cap is reached
    if inventory == 500:
        print("\nMaximum inventory capacity reached.")
        break

# Generate final report
generate_report(inventory, deliveries_processed, failed_entries)