import  sys

def capital_state(capital_name) -> str:
    capital_cities = {
    "Salem": "OR",
    "Montgomery": "AL",
    "Trenton": "NJ",
    "Denver": "CO"
    }
    states = {
    "OR" : "Oregon",
    "AL" : "Alabama",
    "NJ": "New Jersey",
    "CO" : "Colorado"
    }
    return states.get(capital_cities.get(capital_name, ""), "Capital not found")

def state():
    if len(sys.argv) != 2:
        print("Usage: python state.py <capital_name>")
        return

    capital_name = sys.argv[1]

    state = capital_state(capital_name)
    if state == "Capital not found": print(f"{capital_name} is not a capital city.")
    else: print(f"{capital_name} is the capital of {state}.")

if __name__ == '__main__':
    state()