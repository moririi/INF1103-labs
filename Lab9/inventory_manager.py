import csv
import json
import os
from supplier import Supplier
from product_factory import ProductFactory
from can_be_shipped import CanBeShipped
from inventory import Inventory, LINE
from order import Order


INVENTORY_FILE = "inventory.json"
SUPPLIER_FILE = "suppliers.json"

DEFAULT_SUPPLIERS = [
    {"id": "S001", "name": "TechSource Pte Ltd", "email": "sales@techsource.sg"},
    {"id": "S002", "name": "SoftPlus", "email": "support@softplus.sg"},
]

DEFAULT_INVENTORY = [
    {"type": "physical", "id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "weight": 2.0, "supplier_id": "S001"},
    {"type": "physical", "id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "weight": 0.1, "supplier_id": "S001"},
    {"type": "physical", "id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25, "weight": 0.8, "supplier_id": "S001"},
    {"type": "digital", "id": "D001", "name": "Antivirus Licence", "price": 49.90, "stock": 100, "download_size": 350, "supplier_id": "S002"},
]

UNASSIGNED_SUPPLIER = Supplier("S000", "Unassigned", "-")


def read_json(filename: str, default: list[dict]) -> list[dict]:
    if os.path.exists(filename):
        print(f"{filename} found.")
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"{filename} is empty or having issues.  Using defaults.")
            return default
    print(f"{filename} not found.  Using defaults.")
    return default


def load_suppliers() -> dict[str, Supplier]:
    data = read_json(SUPPLIER_FILE, DEFAULT_SUPPLIERS)
    return {s["id"]: Supplier.from_dict(s) for s in data}


def build_inventory(data: list[dict], suppliers: dict[str, Supplier]) -> Inventory:
    inventory = Inventory()
    for p in data:
        supplier = suppliers.get(p.get("supplier_id"), UNASSIGNED_SUPPLIER)
        try:
            product = ProductFactory.create(p.get("type", ""), p["id"], p["name"],
                                            p["price"], p["stock"], supplier,
                                            weight=p.get("weight", 0.0),
                                            download_size=p.get("download_size", 0.0))
        except KeyError as error:
            # one bad entry shouldn't stop the whole inventory from loading
            print(f"Skipped {p.get('id')}: missing field {error}")
            continue
        except ValueError as error:
            print(f"Skipped {p.get('id')}: {error}")
            continue
        inventory.add_product(product)
    return inventory


def load_inventory(suppliers: dict[str, Supplier]) -> Inventory:
    data = read_json(INVENTORY_FILE, DEFAULT_INVENTORY)
    print("Inventory loaded successfully.")
    return build_inventory(data, suppliers)


def save_all(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    with open(INVENTORY_FILE, "w") as file:
        json.dump([p.to_dict() for p in inventory.get_all_products()], file, indent=4)
    with open(SUPPLIER_FILE, "w") as file:
        json.dump([s.to_dict() for s in suppliers.values()], file, indent=4)


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Read products from a CSV file. Bad rows are reported and skipped."""
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                except ValueError as error:
                    # one bad row is reported, then we carry on with the next one
                    print(f"Skipped line {line_number} {row}: {error}")
                    continue
                inventory.add_product(product)
                loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def get_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user types a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_stock(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Invalid input.  Please enter a whole number of 0 or more.")
        else:
            return int(value)


def get_product_type() -> str:
    while True:
        print("1.  Physical Product")
        print("2.  Digital Product")
        choice = input("Product Type: ").strip()
        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"
        print("Please enter 1 or 2.")


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    show_suppliers(suppliers)
    while True:
        supplier_id = get_text("Supplier ID: ").upper()
        if supplier_id in suppliers:
            return suppliers[supplier_id]
        print("Supplier not found, pick one from the list.")


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("Add New Product")
    product_type = get_product_type()
    product_id = get_text("Product ID: ").upper()
    if inventory.find_product(product_id) is not None:
        print(f"Product ID {product_id} already exists.")
        return
    name = get_text("Product Name: ")
    price = get_positive_float("Price: ")
    stock = get_stock("Stock Quantity: ")
    supplier = choose_supplier(suppliers)

    weight = 0.0
    download_size = 0.0
    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
    else:
        download_size = get_positive_float("Download Size (MB): ")

    product = ProductFactory.create(product_type, product_id, name, price, stock,
                                    supplier, weight=weight, download_size=download_size)

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("Update Stock")
    product = inventory.find_product(get_text("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    if product.update_stock(get_stock("New Stock Quantity: ")):
        print("Stock updated successfully!")


def show_search(inventory: Inventory) -> None:
    print("Search Product")
    product = inventory.find_product(get_text("Enter Product ID: "))
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


def remove_product(inventory: Inventory) -> None:
    print("Remove Product")
    removed = inventory.remove_product(get_text("Enter Product ID: "))
    if removed is None:
        print("Product not found.")
        return
    print(f"{removed.get_name()} removed from the inventory.")


def show_suppliers(suppliers: dict[str, Supplier]) -> None:
    print("Suppliers")
    print(LINE)
    for s in suppliers.values():
        s.display_information()
    print(LINE)


def add_supplier(suppliers: dict[str, Supplier]) -> None:
    print("Add New Supplier")
    supplier_id = get_text("Supplier ID: ").upper()
    if supplier_id in suppliers:
        print(f"Supplier {supplier_id} already exists.")
        return
    name = get_text("Supplier Name: ")
    email = get_text("Contact Email: ")
    suppliers[supplier_id] = Supplier(supplier_id, name, email)
    print("Supplier added successfully!")


def create_order(inventory: Inventory, order_count: int) -> None:
    order = Order(f"ORD-{order_count:03d}")
    print(f"Creating {order.get_order_id()} (enter DONE as the Product ID to finish)")

    while True:
        product_id = get_text("Product ID: ").upper()
        if product_id == "DONE":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        if order.has_product(product.get_product_id()):
            print("Already in this order.")
            continue
        quantity = get_stock("Quantity: ")
        if quantity > product.get_stock():
            print(f"Only {product.get_stock()} in stock.")
            continue
        order.add_order_line(product, quantity)

    order.display_order()
    if not order.get_order_lines():
        return

    if input("Confirm order? (y/n): ").strip().lower() == "y":
        for line in order.get_order_lines():
            p = line.get_product()
            p.update_stock(p.get_stock() - line.get_quantity())
        print("Order placed, stock updated.")
    else:
        order.cancel()
        print("Order cancelled.")


def print_menu() -> None:
    print("- MENU -----------")
    print("1.  Display All Products")
    print("2.  Add Product")
    print("3.  Update Stock")
    print("4.  Search Product")
    print("5.  Remove Product")
    print("6.  View Suppliers")
    print("7.  Add Supplier")
    print("8.  Create Order")
    print("9.  Save Inventory")
    print("10. Exit")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    suppliers = load_suppliers()
    inventory = load_inventory(suppliers)
    order_count = 0
    print_menu()

    while True:
        choice = input("Enter option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory, suppliers)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            show_search(inventory)
        elif choice == "5":
            remove_product(inventory)
        elif choice == "6":
            show_suppliers(suppliers)
        elif choice == "7":
            add_supplier(suppliers)
        elif choice == "8":
            order_count += 1
            create_order(inventory, order_count)
        elif choice == "9":
            print("Saving inventory...")
            save_all(inventory, suppliers)
            print(f"Saved to {INVENTORY_FILE} and {SUPPLIER_FILE}.")
        elif choice == "10":
            print("Saving inventory before exit...")
            save_all(inventory, suppliers)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option.  Please enter 1-10.")
            print_menu()


if __name__ == "__main__":
    main()