inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity or 'quit': ")

    # Does user wna quit?
    if stock == "quit":
        print("Exiting the program.")
        break

    # Check for negative numbers
    if stock.startswith("-") and stock[1:].isdigit():
        print("Negative numbers are not allowed.")
        failed_entries += 1
        continue

    # Check for non-integer inputs
    if not stock.isdigit():
        print("Invalid input. Please enter a whole number.")
        failed_entries += 1
        continue

    # Convert string -> integer
    stock = int(stock)

    # Add stock to inventory
    inventory += stock

    # Check if inventory exceeds maximum capacity of 500 units
    if inventory > 500:
        print("Current inventory:", inventory, "units")
        print("Overstocked!! Maximum capacity of 500 units exceeded.")
        break

    # Successful addition of stock
    print("Stock added successfully.")
    print("Current inventory:", inventory, "units")

# Final output
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)