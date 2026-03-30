class HotBeverage:
    def __init__(self, name=None, price=None, description=None):
        self.name = name if name else "hot beverage"
        self.price = price if price else 0.30
        self.description = description if description else "Just some hot water in a cup."

    def __str__(self):
        return f"name : {self.name}\nprice : {self.price:.2f}\ndescription : {self.description}"

class Coffee(HotBeverage):
    def __init__(self, name="coffee", price=0.40, description="A coffee, to stay awake."):
        super().__init__(name, price, description)


class Tea(HotBeverage):
    def __init__(self, name="tea", price=0.30, description="Just some hot water in a cup."):
        super().__init__(name, price, description)


class Chocolate(HotBeverage):
    def __init__(self, name="chocolate", price=0.50, description="Chocolate, sweet chocolate..."):
        super().__init__(name, price, description)


class Cappuccino(HotBeverage):
    def __init__(self, name="cappuccino", price=0.45, description="Un po' di Italia nella sua tazza!"):
        super().__init__(name, price, description)

if __name__ == "__main__":
    try:
        beverage = HotBeverage()
        print(beverage)
        coffee = Coffee()
        print(coffee)
        tea = Tea()
        print(tea)
        chocolate = Chocolate()
        print(chocolate)
        cappuccino = Cappuccino()
        print(cappuccino)
    except Exception as e:
        print(f"Error: {e}")