from django.shortcuts import render


COLOR_SPECS = [
    ("noir", (0, 0, 0)),
    ("rouge", (255, 0, 0)),
    ("bleu", (0, 0, 255)),
    ("vert", (0, 128, 0)),
]


def _to_hex(red: int, green: int, blue: int) -> str:
    return f"#{red:02x}{green:02x}{blue:02x}"


def _build_shades(base_red: int, base_green: int, base_blue: int) -> list[str]:
    shades: list[str] = []
    steps = 50
    for index in range(steps):
        blend = index / (steps - 1)
        red = int(255 + (base_red - 255) * blend)
        green = int(255 + (base_green - 255) * blend)
        blue = int(255 + (base_blue - 255) * blend)
        shades.append(_to_hex(red, green, blue))
    return shades


def ex03_page(request):
    columns = []
    for name, base_color in COLOR_SPECS:
        columns.append(
            {
                "name": name,
                "header_color": _to_hex(*base_color),
                "shades": _build_shades(*base_color),
            }
        )

    rows = []
    for row_index in range(50):
        rows.append([column["shades"][row_index] for column in columns])

    return render(request, "ex03.html", {"columns": columns, "rows": rows})
