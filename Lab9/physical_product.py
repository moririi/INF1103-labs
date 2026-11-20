from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):

    BASE_SHIPPING_FEE: float = 5.00
    FEE_PER_KG: float = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return f"{self.get_name()} will be packed and shipped to the customer."

    def calculate_shipping_cost(self) -> float:
        return round(self.BASE_SHIPPING_FEE + self.__weight * self.FEE_PER_KG, 2)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data