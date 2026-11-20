"""Section 5 predict-first answers (5.1 and 5.2)."""
from inventory import Inventory
from supplier import Supplier
from inventory_manager import get_positive_float, load_products

print("=== 5.1 get_positive_float (try: abc, then -5, then 12.50) ===")
price = get_positive_float("Enter a price: ")
print(f"Returned value: {price}")

print("\n=== 5.2 load_products('products.csv') ===")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
inventory = Inventory("CSV Inventory")
load_products("products.csv", inventory, supplier)
inventory.display_all()

print("\n=== 5.2 load_products with a missing file ===")
load_products("missing_products.csv", Inventory("Empty"), supplier)