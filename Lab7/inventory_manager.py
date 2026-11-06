import json
import os
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory, LINE


INVENTORY_FILE = "inventory.json"

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}

DEFAULT_INVENTORY = [
    {"type": "physical", "id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "weight": 2.0},
    {"type": "physical", "id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "weight": 0.1},
    {"type": "physical", "id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25, "weight": 0.8},
    {"type": "digital", "id": "D001", "name": "Antivirus Licence", "price": 49.90, "stock": 100, "download_size": 350},
]


def build_inventory(data):
    inventory = Inventory()
    for p in data:
        product_class = PRODUCT_TYPES.get(p.get("type"))
        if product_class is None:
            print(f"Skipped {p.get('id')}: unknown product type '{p.get('type')}'.")
            continue
        inventory.add_product(product_class.from_dict(p))
    return inventory


def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
            print("Inventory loaded successfully.")
            return build_inventory(data)
        except json.JSONDecodeError:
            print(f"{INVENTORY_FILE} is empty or having issues.  Starting with default inventory.")
            return build_inventory(DEFAULT_INVENTORY)
    print(f"{INVENTORY_FILE} not found.  Starting with default inventory.")
    return build_inventory(DEFAULT_INVENTORY)


def save_inventory(inventory):
    data = [p.to_dict() for p in inventory.get_all_products()]
    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_positive_number(prompt):
    while True:
        try:
            number = float(input(prompt).strip())
        except ValueError:
            print("Invalid input.  Please enter a number.")
            continue
        if number <= 0:
            print("Value must be greater than 0.")
        else:
            return number


def get_stock(prompt):
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Invalid input.  Please enter a whole number of 0 or more.")
        else:
            return int(value)


def get_product_type():
    while True:
        print("1.  Physical Product")
        print("2.  Digital Product")
        choice = input("Product Type: ").strip()
        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"
        print("Please enter 1 or 2.")


def add_product(inventory):
    print("Add New Product")
    product_type = get_product_type()
    product_id = get_text("Product ID: ").upper()
    if inventory.search_product(product_id) is not None:
        print(f"Product ID {product_id} already exists.")
        return
    name = get_text("Product Name: ")
    price = get_positive_number("Price: ")
    stock = get_stock("Stock Quantity: ")

    if product_type == "physical":
        weight = get_positive_number("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = get_positive_number("Download Size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")
    product = inventory.search_product(get_text("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    if product.update_stock(get_stock("New Stock Quantity: ")):
        print("Stock updated successfully!")


def show_search(inventory):
    print("Search Product")
    product = inventory.search_product(get_text("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"    Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print(LINE)


def print_menu():
    print("- MENU -----------")
    print("1.  Display All Products")
    print("2.  Add Product")
    print("3.  Update Stock")
    print("4.  Search Product")
    print("5.  Save Inventory")
    print("6.  Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()
    print_menu()

    while True:
        choice = input("Enter option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            show_search(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option.  Please enter 1-6.")
            print_menu()


if __name__ == "__main__":
    main()