
def my_var():
    int_v = int(42)
    str_v = str(42)
    str_v2 = str("quarante-deux")
    float_v = float(42)
    bool_v = bool(1)
    list_v = list((42,))
    dict_v = dict({42: 42})
    tuple_v = tuple((42,))
    set_v = set()
    for var in (int_v, str_v, str_v2, float_v, bool_v, list_v, dict_v, tuple_v, set_v):
        print_var(var)

def print_var(var):
    print(f'{var} has a type {type(var)}')

if __name__ == '__main__':
    my_var()