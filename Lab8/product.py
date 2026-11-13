from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Represents ONE product and manages its own state."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> bool:
        """Set a new stock level. Product decides if the value is allowed."""
        if quantity < 0:
            print("Stock cannot be negative.")
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        self.__supplier.display_information()

    def to_dict(self) -> dict:
        """Convert to a dict so it can be saved as JSON."""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass