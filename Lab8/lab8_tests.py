from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


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


if __name__ == "__main__":
    test_association()
    test_aggregation()