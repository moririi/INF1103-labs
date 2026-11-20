import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,
                      BulkDiscount, StudentDiscount)


def make_order_of_250(order_id: str = "ORD-T1") -> Order:
    """Helper: 5 chairs at $50 each = $250 total before discount."""
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    chair = PhysicalProduct("P900", "Chair", 50.00, 20, supplier, 4.0)
    order = Order(order_id)
    order.add_order_line(chair, 5)
    return order


def test_no_discount_is_default() -> None:
    order = make_order_of_250()
    assert isinstance(order.get_discount(), NoDiscount)
    assert order.calculate_total() == 250


def test_bulk_discount_over_threshold() -> None:
    order = make_order_of_250()
    order.set_discount(BulkDiscount(200, 20))
    assert order.calculate_total() == 230


def test_bulk_discount_under_threshold() -> None:
     assert BulkDiscount(200, 20).apply(150) == 150


def test_set_discount_replaces_not_stacks() -> None:
    order = make_order_of_250()
    order.set_discount(BulkDiscount(200, 20))
    assert order.calculate_total() == 230
    order.set_discount(PercentageDiscount(10))
    assert order.calculate_total() == 225


def test_student_discount_without_changing_order() -> None:
    order = make_order_of_250()
    order.set_discount(StudentDiscount())
    assert order.calculate_total() == 237.5


def test_two_orders_can_share_one_discount() -> None:
    shared = PercentageDiscount(10)
    order_a = make_order_of_250("ORD-A")
    order_b = make_order_of_250("ORD-B")
    order_a.set_discount(shared)
    order_b.set_discount(shared)

    assert order_a.get_discount() is order_b.get_discount()
    assert order_a.calculate_total() == 225
    assert order_b.calculate_total() == 225
    order_a.cancel()
    assert order_b.calculate_total() == 225


def test_every_strategy_is_a_discount_strategy() -> None:
    strategies = [NoDiscount(), PercentageDiscount(10), BulkDiscount(200, 20), StudentDiscount()]
    for strategy in strategies:
        assert isinstance(strategy, DiscountStrategy)


def test_order_has_no_discount_if_elif() -> None:
    source = (Path(__file__).resolve().parent.parent / "order.py").read_text()
    for name in ("PercentageDiscount", "BulkDiscount", "StudentDiscount", "discount_type"):
        assert name not in source

if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_") and callable(func):
            func()
            print(f"PASSED {name}")
