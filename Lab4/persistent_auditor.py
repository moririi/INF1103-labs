ORDERS_FILE = "orders.txt"
FIRST_ORDER_ID = 1001


def load_inventory():
    """Read saved orders from disk into a list of [id, name, quantity]."""
    orders = []
    try:
        with open(ORDERS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:  # skip blank lines
                    orders.append(line.split(","))
    except FileNotFoundError:
        pass  # no file yet -> start with an empty order list
    return orders


def display_orders(orders):
    """Print every order currently in the list."""
    print("Current Orders:\n")
    if not orders:
        print("(no orders yet)")
    for order in orders:
        print(", ".join(order))


def generate_new_id(orders):
    """Return the highest existing order ID + 1."""
    if not orders:
        return FIRST_ORDER_ID
    ids = []
    for order in orders:
        ids.append(int(order[0]))  # convert: max() on strings compares alphabetically
    return max(ids) + 1


def get_product_name():
    """Ask for a product name until a non-empty, comma-free one is given."""
    while True:
        name = input("Enter Product Name: ").strip()
        if not name:
            print("Product name cannot be empty.")
        elif "," in name:
            print("Product name cannot contain commas.")
        else:
            return name


def get_quantity():
    """Ask for a quantity until a positive whole number is given."""
    while True:
        quantity = input("Enter Quantity: ").strip()
        if quantity.startswith("-") and quantity[1:].isdigit():
            print("Negative numbers are not allowed.")
        elif not quantity.isdigit():
            print("Invalid input. Please enter a whole number.")
        elif int(quantity) == 0:
            print("Quantity must be at least 1.")
        else:
            return int(quantity)


def save_inventory(order):
    """Append one order to the orders file."""
    with open(ORDERS_FILE, "a") as file:
        file.write(",".join(order) + "\n")


# Input: load saved data and ask for the new order
orders = load_inventory()
display_orders(orders)
print()

product_name = get_product_name()
quantity = get_quantity()

# Process: build the new order and add it to the list
new_id = generate_new_id(orders)
new_order = [str(new_id), product_name, str(quantity)]
orders.append(new_order)

# Output: confirm and write to disk
print("\nNew Order Added:")
print(",".join(new_order))

save_inventory(new_order)
print(f"\nOrder successfully saved to {ORDERS_FILE}")