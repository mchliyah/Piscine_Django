import sys, os, re

def load_context(settings_path):
    context = {}
    with open(settings_path, "r", encoding="utf-8") as settings_file:
        settings_code = settings_file.read()
    exec(settings_code, {}, context)
    return {
        key: value
        for key, value in context.items()
        if not key.startswith("__") and not callable(value)
    }


def render_template(template_content, context):
    def replace_variable(match):
        variable_name = match.group(1).strip()
        return str(context.get(variable_name, match.group(0)))

    return re.sub(r"\{\s*([a-zA-Z_]\w*)\s*\}", replace_variable, template_content)


def main():
    if len(sys.argv) != 2:
        print("Error: wrong number of arguments")
        return 1

    template_path = sys.argv[1]
    if not template_path.endswith(".template"):
        print("Error: input file must have a .template extension")
        return 1

    if not os.path.isfile(template_path):
        print("Error: input file does not exist")
        return 1

    template_dir = os.path.dirname(template_path) or "."
    settings_path = os.path.join(template_dir, "settings.py")
    if not os.path.isfile(settings_path):
        settings_path = "settings.py"
    if not os.path.isfile(settings_path):
        print("Error: settings.py not found")
        return 1

    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()

    context = load_context(settings_path)
    rendered_content = render_template(template_content, context)

    output_path = template_path[:-9] + ".html"
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered_content)

    return 0


if __name__ == "__main__":
    sys.exit(main())

