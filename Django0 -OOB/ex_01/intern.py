class Intern:
    
    def __init__(self, name=None):
        self.name = name if name else "My name? I’m nobody, an intern, I have no name."

    def __str__(self):
        return self.name

    class coffee:
        def __str__(self):
            return "This is the worst coffee you’ve ever tasted."
    def Work(self):
        return "I’m just an intern, I can’t do that..."
    def Make_coffee(self):
        return self.coffee()

if __name__ == "__main__":
    try:
        no_name = Intern()
        print(no_name)
        print(no_name.Work())
        print(no_name.Make_coffee())
        named_intern = Intern("mchliyah")
        print(named_intern)
        print(named_intern.Work())
        print(named_intern.Make_coffee())
    except Exception as e:
        print(f"Error: {e}")