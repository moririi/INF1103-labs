from product import Product

LINE = "-" * 48


class Inventory:
    """Manages a COLLECTION of Product objects."""

    def __init__(self, name: str = "Main Inventory"):
        self.__name: str = name
        self.__products: list[Product] = []

    def get_name(self) -> str:
        return self.__name

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with this ID, or None if not found."""
        for p in self.__products:
            if p.get_product_id().upper() == product_id.upper():
                return p
        return None

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def display_all(self) -> None:
        print(f"{self.__name}")
        print(LINE)
        if not self.__products:
            print("(no products yet)")
        for p in self.__products:
            p.display_information()
        print(LINE)

    def get_all_products(self) -> list[Product]:
        return self.__products