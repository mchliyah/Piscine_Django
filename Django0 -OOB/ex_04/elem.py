
class Text(str):
    def __str__(self):
        return (
            super().__str__()
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("\n", "\n<br />\n")
        )


class Elem:
    class ValidationError(Exception):
        pass

    def __init__(self, tag="div", attr={}, content=None, tag_type="double"):
        self.tag = tag
        self.attr = attr
        self.tag_type = tag_type
        self.content = []

        if not isinstance(self.tag, str) or not isinstance(self.attr, dict):
            raise Elem.ValidationError
        if self.tag_type not in ("double", "simple"):
            raise Elem.ValidationError

        if content is not None:
            self.add_content(content)

    def __str__(self):
        if self.tag_type == "double":
            return (
                "<"
                + self.tag
                + self.__make_attr()
                + ">"
                + self.__make_content()
                + "</"
                + self.tag
                + ">"
            )
        return "<" + self.tag + self.__make_attr() + " />"

    def __make_attr(self):
        result = ""
        for pair in sorted(self.attr.items()):
            result += " " + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_content(self):
        if len(self.content) == 0:
            return ""
        result = "\n"
        for elem in self.content:
            result += "  " + str(elem).replace("\n", "\n  ") + "\n"
        return result

    def add_content(self, content):
        if self.tag_type == "simple" or not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text("")]
        elif content != Text(""):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        return (
            isinstance(content, Elem)
            or type(content) == Text
            or (
                type(content) == list
                and all([type(elem) == Text or isinstance(elem, Elem) for elem in content])
            )
        )


if __name__ == "__main__":
    page = Elem(
        "html",
        content=[
            Elem("head", content=Elem("title", content=Text('"Hello ground!"'))),
            Elem(
                "body",
                content=[
                    Elem("h1", content=Text('"Oh no, not again!"')),
                    Elem(
                        "img",
                        attr={"src": "http://i.imgur.com/pfp3T.jpg"},
                        tag_type="simple",
                    ),
                ],
            ),
        ],
    )
    print(page)

