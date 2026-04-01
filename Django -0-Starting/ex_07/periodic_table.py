#python3
from pathlib import Path

def parse_periodic_table(file_path):
    elements = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            name, data = line.split("=", 1) # Split the line into key-value pairs
            name = name.strip()
            data_parts = data.split(",")
            
            # Extract the required fields
            position = int(data_parts[0].split(":")[1].strip())
            number = int(data_parts[1].split(":")[1].strip())
            symbol = data_parts[2].split(":")[1].strip()
            molar = data_parts[3].split(":")[1].strip()
            electron = data_parts[4].split(":")[1].strip()
            
            # the dictionary element 
            elements.append({
                "name": name,
                "position": position,
                "number": number,
                "symbol": symbol,
                "mass": molar,
                "electron": electron,
            })
    return elements

def build_grid(elements, cols=18):
    grid = []
    current_row = [None] * cols
    previous_position = -1

    for element in elements:
        position = element["position"]

        # A new row starts when the periodic-table column order wraps around.
        if previous_position != -1 and position <= previous_position:
            grid.append(current_row)
            current_row = [None] * cols

        current_row[position] = element
        previous_position = position

    grid.append(current_row)
    return grid


def generate_html(elements):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Periodic Table</title>
</head>
<body>
    <h3>Periodic Table of Elements</h3>
    <table style="border-collapse: collapse;">
"""

    grid = build_grid(elements)

    # Generate table rows and cells
    for row in grid:
        html += "        <tr>\n"
        for cell in row:
            if cell:
                electron_label = "electron" if cell["number"] == 1 else "electrons"
                html += f"""            <td style="border: 1px solid black; padding:10px; text-align:center; vertical-align:top;">
                <h4>{cell['name']}</h4>
                <ul>
                    <li>No {cell['number']}</li>
                    <li>{cell['symbol']}</li>
                    <li>{cell['mass']}</li>
                    <li>{cell['electron']} {electron_label}</li>
                </ul>
            </td>\n"""
            else:
                html += "            <td style=\"border: 1px solid black; padding:10px;\"></td>\n"
        html += "        </tr>\n"

    html += """
    </table>
</body>
</html>
"""
    return html

def periodic_table():
    base_dir = Path(__file__).resolve().parent

    elements = parse_periodic_table(base_dir / "periodic_table.txt")

    html_content = generate_html(elements)

    output_path = base_dir / "periodic_table.html" # Write the HTML content to a file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML file 'periodic_table.html' has been created.")

if __name__ == "__main__":
    periodic_table()