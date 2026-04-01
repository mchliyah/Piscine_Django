from elem import Elem, Text
from elements import (
	Body,
	Br,
	Div,
	H1,
	H2,
	Head,
	Hr,
	Html,
	Img,
	Li,
	Meta,
	Ol,
	P,
	Span,
	Table,
	Td,
	Th,
	Title,
	Tr,
	Ul,
)


class Page:
	def __init__(self, root):
		if not isinstance(root, Elem):
			raise TypeError("Page root must inherit Elem")
		self.root = root

	def __str__(self):
		html = str(self.root)
		if isinstance(self.root, Html):
			return "<!DOCTYPE html>\n" + html
		return html

	def write_to_file(self, filename):
		with open(filename, "w", encoding="utf-8") as file:
			file.write(str(self))

	def is_valid(self):
		return self._validate_node(self.root)

	def _children_of(self, node):
		if isinstance(node, Text):
			return []
		return node.content

	def _validate_node(self, node):
		allowed = (
			Html,
			Head,
			Body,
			Title,
			Meta,
			Img,
			Table,
			Th,
			Tr,
			Td,
			Ul,
			Ol,
			Li,
			H1,
			H2,
			P,
			Div,
			Span,
			Hr,
			Br,
			Text,
		)
		if not isinstance(node, allowed):
			return False

		children = self._children_of(node)

		if isinstance(node, Html):
			if len(children) != 2 or not isinstance(children[0], Head) or not isinstance(children[1], Body):
				return False

		if isinstance(node, Head):
			if len(children) != 1 or not isinstance(children[0], Title):
				return False

		if isinstance(node, (Body, Div)):
			if not all(isinstance(child, (H1, H2, Div, Table, Ul, Ol, Span, Text)) for child in children):
				return False

		if isinstance(node, (Title, H1, H2, Li, Th, Td)):
			if len(children) != 1 or not isinstance(children[0], Text):
				return False

		if isinstance(node, P):
			if not all(isinstance(child, Text) for child in children):
				return False

		if isinstance(node, Span):
			if not all(isinstance(child, (Text, P)) for child in children):
				return False

		if isinstance(node, (Ul, Ol)):
			if len(children) == 0 or not all(isinstance(child, Li) for child in children):
				return False

		if isinstance(node, Tr):
			if len(children) == 0:
				return False
			has_th = all(isinstance(child, Th) for child in children)
			has_td = all(isinstance(child, Td) for child in children)
			if not (has_th or has_td):
				return False

		if isinstance(node, Table):
			if len(children) == 0 or not all(isinstance(child, Tr) for child in children):
				return False

		for child in children:
			if not self._validate_node(child):
				return False
		return True


def _self_test():
	valid_page = Page(
		Html(
			[
				Head(Title('"Hello ground!"')),
				Body(
					[
						H1('"Oh no, not again!"'),
						Div([Span("small note"), Ul([Li("a"), Li("b")])]),
					]
				),
			]
		)
	)
	assert valid_page.is_valid() is True
	assert str(valid_page).startswith("<!DOCTYPE html>\n<html>")

	invalid_html = Page(Html([Body(), Head(Title("x"))]))
	assert invalid_html.is_valid() is False

	invalid_head = Page(Html([Head([Title("x"), Title("y")]), Body()]))
	assert invalid_head.is_valid() is False

	invalid_body = Page(Html([Head(Title("x")), Body([Img(attr={"src": "x"})])]))
	assert invalid_body.is_valid() is False

	invalid_tr = Page(Html([Head(Title("x")), Body([Table([Tr([Th("h"), Td("v")])])])]))
	assert invalid_tr.is_valid() is False

	non_html_page = Page(Div("content"))
	assert non_html_page.is_valid() is True
	assert not str(non_html_page).startswith("<!DOCTYPE html>")

	valid_page.write_to_file("page_test.html")


if __name__ == "__main__":
	_self_test()
