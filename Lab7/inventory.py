LINE = "-" * 48


class Inventory:
    """Manages a COLLECTION of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        """Return the Product with this ID, or None if not found."""
        for p in self.__products:
            if p.get_product_id().upper() == product_id.upper():
                return p
        return None

    def display_all(self):
        print("Current Inventory")
        print(LINE)
        if not self.__products:
            print("(no products yet)")
        for p in self.__products:
            p.display_information()
        print(LINE)

    def get_all_products(self):
        return self.__products