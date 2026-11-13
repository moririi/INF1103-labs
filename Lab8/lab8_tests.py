from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from product import Product


def test_association() -> None:
    print("=== Section 2 - Association ===")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    guitar = PhysicalProduct("P100", "Guitar", 299.90, 5, supplier, 3.5)
    windows = DigitalProduct("D100", "Windows 11", 199.00, 50, supplier, 5400)

    print("Supplier info through each product:")
    guitar.get_supplier().display_information()
    windows.get_supplier().display_information()

    print(f"guitar is supplier? {guitar is supplier}")
    print(f"both products point to the same supplier? "
          f"{guitar.get_supplier() is windows.get_supplier()}")

    del supplier
    print("After del supplier:")
    guitar.get_supplier().display_information()
    windows.get_supplier().display_information()


def test_aggregation() -> None:
    print("\n=== Section 3 - Aggregation ===")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    amp = PhysicalProduct("P101", "Amplifier", 450.00, 3, supplier, 15)

    inventory_a = Inventory("Inventory A")
    inventory_b = Inventory("Inventory B")

    inventory_a.add_product(amp)
    inventory_a.display_all()

    removed = inventory_a.remove_product("P101")
    print(f"Still in A? {inventory_a.find_product('P101') is not None}")

    print("Using amp after removing it from A:")
    amp.update_stock(10)
    print(f"  {amp.get_name()} stock is now {amp.get_stock()}")
    print(f"  removed is amp? {removed is amp}")

    inventory_b.add_product(amp)
    print(f"Same object now in B? {inventory_b.find_product('P101') is amp}")
    inventory_b.display_all()

    inventory_b.remove_product("P101")
    print(f"B is empty ({len(inventory_b.get_all_products())} items) "
          f"but amp still exists: {amp.get_name()}")

def test_composition() -> None:
    print("\n=== Section 4 - Composition ===")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.0)
    antivirus = DigitalProduct("D001", "Antivirus Licence", 49.90, 100, supplier, 350)

    order_1 = Order("ORD-001")
    order_1.add_order_line(laptop, 2)
    order_1.add_order_line(antivirus, 3)
    order_1.display_order()

    order_2 = Order("ORD-002")
    order_2.add_order_line(laptop, 1)
    order_2.display_order()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print("Same Laptop in two orders:")
    print(f"  same OrderLine? {line_1 is line_2}  ({id(line_1)} vs {id(line_2)})")
    print(f"  same Product?   {line_1.get_product() is line_2.get_product()}  "
          f"({id(line_1.get_product())} vs {id(line_2.get_product())})")

    print("Removing Antivirus line from ORD-001:")
    order_1.remove_order_line("D001")
    order_1.display_order()

    print("Cancelling ORD-001:")
    order_1.cancel()
    print(f"  ORD-001 lines left: {len(order_1.get_order_lines())}")
    print(f"  Laptop still exists: {laptop.get_name()}, stock {laptop.get_stock()}")

def show_product_details(product: Product) -> None:
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")


def test_lsp() -> None:
    print("\n=== Section 6 - Liskov Substitution ===")
    supplier = Supplier("S002", "SoftPlus", "support@softplus.sg")
    picks = PhysicalProduct("P102", "Guitar Picks", 4.90, 100, supplier, 0.1)
    vpn = DigitalProduct("D002", "VPN 6-Month Plan", 35.00, 40, supplier, 80)

    for product in (picks, vpn):
        show_product_details(product)
        ok = product.update_stock(20)
        print(f"    update_stock(20) -> {ok}, stock now {product.get_stock()}")
        ok = product.update_stock(-5)
        print(f"    update_stock(-5) -> {ok}, stock still {product.get_stock()}\n")

    inventory = Inventory("LSP Inventory")
    inventory.add_product(picks)
    inventory.add_product(vpn)
    print(f"find_product works for both: {inventory.find_product('P102').get_name()}, "
          f"{inventory.find_product('D002').get_name()}")

def test_polymorphism() -> None:
    print("\n=== Section 7 - Polymorphism ===")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    inventory = Inventory("Mixed Inventory")
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, supplier, 0.1))
    inventory.add_product(DigitalProduct("D003", "Photo Editor", 120.00, 25, supplier, 1500))

    for product in inventory.get_all_products():
        product.display_information()
        print(f"    Fulfilment: {product.get_fulfilment_info()}")


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()