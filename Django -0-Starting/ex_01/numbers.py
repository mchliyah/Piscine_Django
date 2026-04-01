
def numbers():
    filename = 'numbers.txt'
    try:
        with open(filename, 'r') as f: # Open the file for reading
            content = f.read()
            for num_str in content.strip().split(','):
                if num_str.strip().isdigit():
                    print(num_str.strip()) # Print the number if it's valid
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

if __name__ == '__main__':
    numbers()