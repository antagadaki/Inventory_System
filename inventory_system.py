import json
from abc import ABC, abstractmethod

# Base class
class Product(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

# Electronics
class Electronics(Product):
    def __init__(self, name, price, brand, warranty):
        super().__init__(name, price)
        self.brand = brand
        self.warranty = warranty

    def display(self):
        print(f"Electronics: {self.name}, ${self.price}, Brand: {self.brand}, Warranty: {self.warranty} years")

    def to_dict(self):
        return {"category": "Electronics", "name": self.name, "price": self.price, "brand": self.brand, "warranty": self.warranty}

# Clothing
class Clothing(Product):
    def __init__(self, name, price, sizes, material, colors):
        super().__init__(name, price)
        self.sizes = sizes
        self.material = material
        self.colors = colors

    def display(self):
        print(f"Clothing: {self.name}, ${self.price}, Sizes: {', '.join(self.sizes)}, Material: {self.material}, Colors: {', '.join(self.colors)}")

    def to_dict(self):
        return {"category": "Clothing", "name": self.name, "price": self.price, "sizes": self.sizes, "material": self.material, "colors": self.colors}

# Grocery
class Grocery(Product):
    def __init__(self, name, price, weight, expiration_date):
        super().__init__(name, price)
        self.weight = weight
        self.expiration_date = expiration_date

    def display(self):
        print(f"Grocery: {self.name}, ${self.price}, Weight: {self.weight}kg, Exp: {self.expiration_date}")

    def to_dict(self):
        return {"category": "Grocery", "name": self.name, "price": self.price, "weight": self.weight, "expiration_date": self.expiration_date}

# Inventory management
inventory = []

def save_inventory():
    with open("inventory.json", "w") as f:
        json.dump([item.to_dict() for item in inventory], f, indent=4)

def load_inventory():
    try:
        with open("inventory.json", "r") as f:
            items = json.load(f)
            for item in items:
                if item["category"] == "Electronics":
                    inventory.append(Electronics(item["name"], item["price"], item["brand"], item["warranty"]))
                elif item["category"] == "Clothing":
                    inventory.append(Clothing(item["name"], item["price"], item["sizes"], item["material"], item["colors"]))
                elif item["category"] == "Grocery":
                    inventory.append(Grocery(item["name"], item["price"], item["weight"], item["expiration_date"]))
    except FileNotFoundError:
        pass

def add_product():
    category = input("Category (Electronics/Clothing/Grocery): ").strip().lower()
    name = input("Name: ")
    price = float(input("Price: "))

    if category == "electronics":
        brand = input("Brand: ")
        warranty = int(input("Warranty (years): "))
        inventory.append(Electronics(name, price, brand, warranty))

    elif category == "clothing":
        sizes = input("Sizes (comma-separated): ").split(',')
        material = input("Material: ")
        colors = input("Colors (comma-separated): ").split(',')
        inventory.append(Clothing(name, price, [s.strip() for s in sizes], material, [c.strip() for c in colors]))

    elif category == "grocery":
        weight = float(input("Weight (kg): "))
        expiration_date = input("Expiration Date (YYYY-MM-DD): ")
        inventory.append(Grocery(name, price, weight, expiration_date))
    else:
        print("Invalid category.")
        return
    save_inventory()
    print("Product added.")

def view_inventory():
    if not inventory:
        print("Inventory is empty.")
    for item in inventory:
        item.display()

def modify_product():
    name = input("Enter the name of the product to modify: ")
    for item in inventory:
        if item.name.lower() == name.lower():
            item.price = float(input("Enter new price: "))
            save_inventory()
            print("Price updated.")
            return
    print("Product not found.")

def menu():
    load_inventory()
    while True:
        print("\n1. Add Product\n2. View Inventory\n3. Modify Product\n4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            modify_product()
        elif choice == "4":
            save_inventory()
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()
