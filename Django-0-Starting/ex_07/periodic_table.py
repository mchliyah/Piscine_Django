#python3
import sys

def parse_periodic_table(file_path):
    elements = []
    with open(file_path, "r") as file:
        for line in file:
            # Split the line into key-value pairs
            name, data = line.split("=", 1)
            name = name.strip()
            data_parts = data.split(",")
            
            # Extract the required fields
            position = int(data_parts[0].split(":")[1].strip())
            number = int(data_parts[1].split(":")[1].strip())
            symbol = data_parts[2].split(":")[1].strip()
            molar = data_parts[3].split(":")[1].strip()
            electron = data_parts[4].split(":")[1].strip()
            
            # Append the element as a dictionary
            elements.append({
                "name": name,
                "position": position,
                "number": number,
                "symbol": symbol,
                "mass": molar,
                "electron": electron,
            })
    return elements

def generate_html(elements):
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Periodic Table</title>
    <style>
        table { border-collapse: collapse; }
        td { border: 1px solid black; padding: 10px; text-align: center; vertical-align: top; }
        h4 { margin: 5px 0; }
        ul { padding: 0; list-style-type: none; }
    </style>
</head>
<body>
    <h1>Periodic Table of Elements</h1>
    <table>
"""

    # Create a 7x18 grid (7 rows, 18 columns) for the periodic table 
    max_rows, max_cols = 7, 18
    grid = [[None for _ in range(max_cols)] for _ in range(max_rows)]

    # Place elements in their respective positions
    for element in elements:
        row, col = divmod(element["position"], max_cols)
        grid[row][col] = element

    # Generate table rows and cells
    for row in grid:
        html += "        <tr>\n"
        for cell in row:
            if cell:
                html += f"""            <td>
                <h4>{cell['name']}</h4>
                <ul>
                    <li>No {cell['number']}</li>
                    <li>{cell['symbol']}</li>
                    <li>{cell['mass']}</li>
                    <li>{cell['electron']}</li>
                </ul>
            </td>\n"""
            else:
                html += "            <td></td>\n"
        html += "        </tr>\n"

    html += """
    </table>
</body>
</html>
"""
    return html

def periodic_table():
    # Parse the periodic table data from the file
    elements = parse_periodic_table("periodic_table.txt")

    # Generate the HTML content
    html_content = generate_html(elements)

    # Write the HTML content to a file
    with open("periodic_table.html", "w") as file:
        file.write(html_content)
    print("HTML file 'periodic_table.html' has been created.")

if __name__ == "__main__":
    periodic_table()