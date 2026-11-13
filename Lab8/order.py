from product import Product


class OrderLine:

    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_line(self) -> None:
        print(f"  {self.__product.get_name():<20} x{self.__quantity:<4} "
              f"${self.calculate_subtotal():>9.2f}")


class Order:

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> bool:
        if quantity <= 0:
            print("Quantity must be at least 1.")
            return False
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)
        return True

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.__order_lines:
            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return True
        return False

    def has_product(self, product_id: str) -> bool:
        return any(line.get_product().get_product_id() == product_id
                   for line in self.__order_lines)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("  (no items)")
        for line in self.__order_lines:
            line.display_line()
        print(f"  {'TOTAL':<26} ${self.calculate_total():>9.2f}")

    def cancel(self) -> None:
        self.__order_lines.clear()