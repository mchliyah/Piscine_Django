from elem import Elem, Text


def _normalize_item(item):
	if isinstance(item, (Elem, Text)):
		return item
	if isinstance(item, (str, int, float, bool)):
		return Text(str(item))
	return item


def _normalize_content(content):
	if content is None:
		return None
	if isinstance(content, list):
		return [_normalize_item(item) for item in content]
	return _normalize_item(content)


class Html(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="html", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Head(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="head", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Body(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="body", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Title(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="title", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Meta(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="meta", attr=attr or {}, content=None, tag_type="simple")


class Img(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="img", attr=attr or {}, content=None, tag_type="simple")


class Table(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="table", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Th(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="th", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Tr(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="tr", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Td(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="td", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Ul(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="ul", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Ol(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="ol", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Li(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="li", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class H1(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="h1", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class H2(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="h2", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class P(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="p", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Div(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="div", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Span(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="span", attr=attr or {}, content=_normalize_content(content), tag_type="double")


class Hr(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="hr", attr=attr or {}, content=None, tag_type="simple")


class Br(Elem):
	def __init__(self, content=None, attr=None):
		super().__init__(tag="br", attr=attr or {}, content=None, tag_type="simple")


html = Html
head = Head
body = Body
title = Title
meta = Meta
img = Img
table = Table
th = Th
tr = Tr
td = Td
ul = Ul
ol = Ol
li = Li
h1 = H1
h2 = H2
p = P
div = Div
span = Span
hr = Hr
br = Br


def _self_test():
	assert str(Html([Head(), Body()])) == "<html>\n  <head></head>\n  <body></body>\n</html>"
	assert str(Img(attr={"src": "x.png"})) == '<img src="x.png" />'
	assert str(Br()) == "<br />"
	assert str(Hr()) == "<hr />"
	assert str(P("hello")) == "<p>\n  hello\n</p>"
	assert str(Ul([Li("a"), Li("b")])) == "<ul>\n  <li>\n    a\n  </li>\n  <li>\n    b\n  </li>\n</ul>"
	assert str(Table([Tr([Th("h"), Td("v")])])) == (
		"<table>\n"
		"  <tr>\n"
		"    <th>\n"
		"      h\n"
		"    </th>\n"
		"    <td>\n"
		"      v\n"
		"    </td>\n"
		"  </tr>\n"
		"</table>"
	)


if __name__ == "__main__":
	_self_test()
	print("Self-test: OK")

	page = Html(
		[
			Head(Title('"Hello ground!"')),
			Body(
				[
					H1('"Oh no, not again!"'),
					Img(attr={"src": "http://i.imgur.com/pfp3T.jpg"}),
				]
			),
		]
	)
	print(page)
