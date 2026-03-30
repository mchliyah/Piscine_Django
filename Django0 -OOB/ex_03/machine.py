import beverages
import random

class CoffeeMachine:
    class EmptyCup(beverages.HotBeverage):
        def __init__(self):
            super().__init__(
                name="empty cup",
                price=0.90,
                description="An empty cup?! Gimme my money back!"
            )

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self._served_since_repair = 0
        self._is_broken = False

    def repair(self):
        self._served_since_repair = 0
        self._is_broken = False

    def serve(self, beverage_class):
        if self._is_broken:
            raise CoffeeMachine.BrokenMachineException()

        if not isinstance(beverage_class, type) or not issubclass(
            beverage_class,
            beverages.HotBeverage
        ):
            raise TypeError("serve() expects a class derived from HotBeverage")

        served_drink = random.choice([beverage_class(), CoffeeMachine.EmptyCup()])
        self._served_since_repair += 1

        if self._served_since_repair >= 10:
            self._is_broken = True

        return served_drink


if __name__ == "__main__":
    machine = CoffeeMachine()
    drink_types = [
        beverages.Coffee,
        beverages.Tea,
        beverages.Chocolate,
        beverages.Cappuccino,
    ]

    breakdowns = 0
    while breakdowns < 2:
        try:
            asked_drink = random.choice(drink_types)
            print(machine.serve(asked_drink))
            print()
        except CoffeeMachine.BrokenMachineException as error:
            print(error)
            print()
            breakdowns += 1
            if breakdowns < 2:
                machine.repair()