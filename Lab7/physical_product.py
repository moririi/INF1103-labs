from product import Product
from can_be_shipped import CanBeShipped
 
class PhysicalProduct(Product, CanBeShipped):

    BASE_SHIPPING_FEE = 5.00
    FEE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return f"{self.get_name()} will be packed and shipped to the customer."

    def calculate_shipping_cost(self):
        return round(self.BASE_SHIPPING_FEE + self.__weight * self.FEE_PER_KG, 2)