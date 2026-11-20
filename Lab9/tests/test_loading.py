import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from supplier import Supplier
from inventory import Inventory
from inventory_manager import get_positive_float, load_products

PROJECT = Path(__file__).resolve().parent.parent
SUPPLIER = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")


def run_and_capture(func, *args) -> str:
    """Run func and return everything it printed."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue()


def test_positive_float_keeps_asking_until_valid() -> None:
    # Predict first 5.1: abc -> -5 -> 12.50
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            value = get_positive_float("Price: ")
    lines = buffer.getvalue().splitlines()
    assert lines == ["Please enter a valid number, e.g. 12.50",
                     "Please enter a number greater than zero."]
    assert value == 12.5


def test_csv_loads_valid_rows_and_skips_bad_ones() -> None:
    # Predict first 5.2: 3 load, service row + 'abc' price row skipped
    inventory = Inventory("CSV")
    output = run_and_capture(load_products, str(PROJECT / "products.csv"), inventory, SUPPLIER)

    ids = [p.get_product_id() for p in inventory.get_all_products()]
    assert ids == ["P001", "D001", "P003"]
    assert "Unknown product type: service" in output
    assert "could not convert string to float: 'abc'" in output

    lines = output.splitlines()
    assert lines[-2] == "3 products loaded."
    assert lines[-1] == "Load attempt finished."


def test_missing_file_is_handled_gracefully() -> None:
    # renamed file: except + finally run, else doesn't
    inventory = Inventory("Empty")
    output = run_and_capture(load_products, "does_not_exist.csv", inventory, SUPPLIER)
    assert output.splitlines() == ["Products file not found: does_not_exist.csv",
                                   "Load attempt finished."]
    assert len(inventory.get_all_products()) == 0


def test_every_except_is_specific() -> None:
    # Section 7: no bare "except:" or "except Exception" anywhere in my code
    for file in PROJECT.glob("*.py"):
        source = file.read_text()
        assert "except:" not in source, file.name
        assert "except Exception" not in source, file.name


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_") and callable(func):
            func()
            print(f"PASSED {name}")