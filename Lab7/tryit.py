from physical_product import PhysicalProduct
from digital_product import DigitalProduct

guitar = PhysicalProduct("P100", "Guitar", 299.90, 5, 3.5)
guitar.display_information()
print(guitar.get_name())
print(guitar.get_weight())

windows = DigitalProduct("D100", "Windows 11", 199.00, 50, 5400)
windows.display_information()
print(windows.get_download_size())