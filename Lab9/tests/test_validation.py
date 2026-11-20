import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order, OrderLine
from inventory_manager import build_inventory

SUPPLIER = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")


def expect_value_error(func, message: str) -> None:
    """Small helper: func() must raise ValueError with this exact message."""
    try:
        func()
        assert False, "should have raised ValueError"
    except ValueError as error:
        assert str(error) == message


def test_price_must_be_greater_than_zero() -> None:
    expect_value_error(lambda: PhysicalProduct("P1", "Lamp", 0, 5, SUPPLIER, 1.0),
                       "Price must be greater than zero.")
    expect_value_error(lambda: PhysicalProduct("P1", "Lamp", -10, 5, SUPPLIER, 1.0),
                       "Price must be greater than zero.")


def test_stock_cannot_be_negative() -> None:
    expect_value_error(lambda: PhysicalProduct("P1", "Lamp", 10, -1, SUPPLIER, 1.0),
                       "Stock quantity cannot be negative.")


def test_zero_stock_is_allowed() -> None:
    lamp = PhysicalProduct("P1", "Lamp", 10, 0, SUPPLIER, 1.0)
    assert lamp.get_stock() == 0


def test_digital_product_follows_same_rule() -> None:
    # Predict first 4 (LSP): the child can't skip the parent's rule
    expect_value_error(lambda: DigitalProduct("D1", "App", 10, -5, SUPPLIER, 100),
                       "Stock quantity cannot be negative.")


def test_order_line_quantity_must_be_positive() -> None:
    lamp = PhysicalProduct("P1", "Lamp", 10, 5, SUPPLIER, 1.0)
    expect_value_error(lambda: OrderLine(lamp, 0), "Quantity must be greater than zero.")
    expect_value_error(lambda: OrderLine(lamp, -3), "Quantity must be greater than zero.")


def test_order_rejects_bad_quantity_without_crashing() -> None:
    lamp = PhysicalProduct("P1", "Lamp", 10, 5, SUPPLIER, 1.0)
    order = Order("ORD-V1")
    assert order.add_order_line(lamp, 0) is False
    assert len(order.get_order_lines()) == 0
    assert order.add_order_line(lamp, 2) is True


def test_bad_json_entries_are_skipped_not_crashing() -> None:
    data = [
        {"type": "physical", "id": "P1", "name": "Lamp", "price": 10, "stock": 5, "weight": 1.0},
        {"type": "physical", "id": "P2", "name": "No Price", "stock": 5, "weight": 1.0},
        {"type": "physical", "id": "P3", "name": "Bad Price", "price": -5, "stock": 5, "weight": 1.0},
    ]
    inventory = build_inventory(data, {"S001": SUPPLIER})
    assert len(inventory.get_all_products()) == 1


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_") and callable(func):
            func()
            print(f"PASSED {name}")