import json
import os
 
INVENTORY_FILE = "inventory.json"
LINE = "-" * 48

#Starting inventory data when inventory.json does not exist
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]

def load_inventory():
    """Load inventory.json if it exists, otherwise start from the default products."""
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as file:
                inventory = json.load(file)
            print("Inventory loaded successfully.")
            return inventory
        except json.JSONDecodeError:
            print(f"{INVENTORY_FILE} is empty or having issues.  Starting with default inventory.")
            return [dict(p) for p in DEFAULT_INVENTORY]
    print(f"{INVENTORY_FILE} not found.  Starting with default inventory.")
    return [dict(p) for p in DEFAULT_INVENTORY]
 

def save_inventory(inventory):
    """Write the whole inventory list to inventory.json."""
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)



# - Input stuff 
def get_text(prompt):
    """Ask until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")
 
 
def get_price(prompt):
    """Ask until a positive number is entered."""
    while True:
        try:
            price = float(input(prompt).strip())
        except ValueError:
            print("Invalid input.  Please enter a number.")
            continue
        if price <= 0:
            print("Price must be greater than 0.")
        else:
            return price
 
 
def get_stock(prompt):
    """Ask until a whole number of 0 or more is entered (0 = sold out)."""
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Invalid input.  Please enter a whole number of 0 or more.")
        else:
            return int(value)


 
# - CRUD functions
def display_all(inventory):
    """Print every product in the inventory."""
    print("Current Inventory")
    print(LINE)
    if not inventory:
        print("(no products yet)")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print(LINE)
 
 
def search_product(inventory, product_id):
    """Return the product dict with this ID, or None if not found."""
    for p in inventory:
        if p["id"].upper() == product_id.upper():
            return p
    return None
 
 
def add_product(inventory):
    """Ask for a new product's details and append it to the inventory."""
    print("Add New Product")
    product_id = get_text("Product ID: ").upper()
    if search_product(inventory, product_id) is not None:
        print(f"Product ID {product_id} already exists.")
        return
    name = get_text("Product Name: ")
    price = get_price("Price: ")
    stock = get_stock("Stock Quantity: ")
    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")
 
 
def update_stock(inventory):
    """Change the stock level of an existing product."""
    print("Update Stock")
    product_id = get_text("Enter Product ID: ")
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    product["stock"] = get_stock("New Stock Quantity: ")  # edits the dict inside the list
    print("Stock updated successfully!")
 
 
def show_search(inventory):
    """Menu wrapper: ask for an ID and print the matching product."""
    print("Search Product")
    product = search_product(inventory, get_text("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)



 # - Menu shii
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
            display_all(inventory)
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
