import sys

def state_capital(state_name) -> str:
    states = {
    "Oregon" : "OR",
    "Alabama" : "AL",
    "New Jersey": "NJ",
    "Colorado" : "CO"
    }
    capital_cities = {
    "OR": "Salem",
    "AL": "Montgomery",
    "NJ": "Trenton",
    "CO": "Denver"
    }
    return capital_cities.get(states.get(state_name, ""), "State not found")

def capital_city():
    if len(sys.argv) != 2:
        print("Usage: python capital_city.py <state_name>")
        return

    state_name = sys.argv[1]

    capital = state_capital(state_name)
    if capital == "State not found": print(f"The capital of {state_name} is {capital}.")
    else: print(f"The capital of {state_name} is {capital}.")

if __name__ == '__main__':
    capital_city()
