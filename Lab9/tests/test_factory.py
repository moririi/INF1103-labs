import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory

SUPPLIER = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")


def test_factory_creates_physical_product() -> None:
    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, SUPPLIER, weight=1.2)
    assert isinstance(lamp, PhysicalProduct)
    assert isinstance(lamp, Product)
    assert lamp.get_weight() == 1.2


def test_factory_creates_digital_product() -> None:
    editor = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, SUPPLIER,
                                   download_size=800)
    assert isinstance(editor, DigitalProduct)
    assert editor.get_download_size() == 800


def test_factory_ignores_case_and_spaces() -> None:
    lamp = ProductFactory.create("  Physical ", "P002", "Lamp", 10.00, 1, SUPPLIER)
    assert isinstance(lamp, PhysicalProduct)


def test_unknown_type_raises_value_error() -> None:
    try:
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, SUPPLIER)
        assert False, "should have raised ValueError"
    except ValueError as error:
        assert str(error) == "Unknown product type: service"


def test_manager_creates_products_through_factory() -> None:
    source = (Path(__file__).resolve().parent.parent / "inventory_manager.py").read_text()
    assert "ProductFactory.create" in source
    assert "PhysicalProduct(" not in source
    assert "DigitalProduct(" not in source


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_") and callable(func):
            func()
            print(f"PASSED {name}")