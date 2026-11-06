from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped

guitar = PhysicalProduct("P100", "Guitar", 299.90, 5, 3.5)
guitar.display_information()
print(guitar.get_name())
print(guitar.get_weight())

windows = DigitalProduct("D100", "Windows 11", 199.00, 50, 5400)
windows.display_information()
print(windows.get_download_size())

print(guitar.get_fulfilment_info())
print(windows.get_fulfilment_info())

amp = PhysicalProduct("P101", "Amplifier", 450.00, 3, 15)
picks = PhysicalProduct("P102", "Guitar Picks", 4.90, 100, 0.1)

print(guitar.calculate_shipping_cost())
print(amp.calculate_shipping_cost())
print(picks.calculate_shipping_cost())

print(isinstance(guitar, CanBeShipped))
print(isinstance(windows, CanBeShipped))