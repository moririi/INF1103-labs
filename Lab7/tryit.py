from physical_product import PhysicalProduct

guitar = PhysicalProduct("P100", "Guitar", 299.90, 5, 3.5)
guitar.display_information()
print(guitar.get_name())
print(guitar.get_weight())