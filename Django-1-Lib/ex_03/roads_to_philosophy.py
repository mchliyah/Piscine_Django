import sys, requests
from bs4 import BeautifulSoup


BASE_URL = "https://en.wikipedia.org"
SEARCH_URL = BASE_URL + "/w/index.php"


def _normalize_title(title):
    return " ".join(title.lower().split())


def _is_tag(node):
    return hasattr(node, "name") and node.name is not None


def _is_valid_article_href(href):
    if not href or not href.startswith("/wiki/"):
        return False
    if "#" in href:
        return False
    target = href[len("/wiki/"):]
    if not target:
        return False
    if ":" in target:
        return False
    return True


def _href_to_title(href):
    if not href.startswith("/wiki/"):
        return ""
    raw = href[len("/wiki/"):]
    raw = raw.replace("_", " ")
    return requests.utils.unquote(raw)


def _extract_redirected_from(soup):
    redirected = soup.find(class_="mw-redirectedfrom")
    if redirected is None:
        return None
    link = redirected.find("a")
    if link is None:
        return None
    text = link.get_text(strip=True)
    return text if text else None


def _extract_main_title(soup):
    heading = soup.find("h1", id="firstHeading")
    if heading is None:
        return None
    title = heading.get_text(strip=True)
    return title if title else None


def _get_article_parser_output(soup):
    content_text = soup.find("div", id="mw-content-text")
    if content_text is None:
        return None

    for child in content_text.find_all(recursive=False):
        if _is_tag(child) and "mw-parser-output" in child.get("class", []):
            return child

    return content_text.find("div", class_="mw-parser-output")


def _is_in_italic(tag):
    parent = tag.parent
    while _is_tag(parent):
        if parent.name in ("i", "em"):
            return True
        parent = parent.parent
    return False


def _is_in_ignored_container(tag):
    parent = tag.parent
    ignored_classes = {
        "hatnote",
        "shortdescription",
        "infobox",
        "navbox",
        "sidebar",
        "thumb",
        "metadata",
        "mw-references-wrap",
    }
    while _is_tag(parent):
        if parent.name in ("table", "sup"):
            return True
        classes = set(parent.get("class", []))
        if classes & ignored_classes:
            return True
        parent = parent.parent
    return False


def _first_valid_link_in_paragraph(paragraph, current_title):
    depth = 0
    current_key = _normalize_title(current_title)
    for node in paragraph.descendants:
        if isinstance(node, str):
            for char in str(node):
                if char == "(":
                    depth += 1
                elif char == ")" and depth > 0:
                    depth -= 1
            continue

        if not _is_tag(node):
            continue
        if node.name != "a":
            continue
        if _is_in_italic(node):
            continue
        if _is_in_ignored_container(node):
            continue

        href = node.get("href", "")
        if depth == 0 and _is_valid_article_href(href):
            href_title = _href_to_title(href)
            if _normalize_title(href_title) == current_key:
                continue
            return href

    return None


def _collect_intro_link_hrefs(soup, current_title):
    content = _get_article_parser_output(soup)
    if content is None:
        return []

    intro_paragraphs = []
    seen = set()
    for node in content.descendants:
        if not _is_tag(node):
            continue
        if node.name == "h2":
            break
        if node.name != "p":
            continue
        if not node.get_text(strip=True):
            continue
        if _is_in_ignored_container(node):
            continue
        node_id = id(node)
        if node_id in seen:
            continue
        seen.add(node_id)
        intro_paragraphs.append(node)

    hrefs = []
    for paragraph in intro_paragraphs:
        depth = 0
        current_key = _normalize_title(current_title)
        for node in paragraph.descendants:
            if isinstance(node, str):
                for char in str(node):
                    if char == "(":
                        depth += 1
                    elif char == ")" and depth > 0:
                        depth -= 1
                continue

            if not _is_tag(node):
                continue
            if node.name != "a":
                continue
            if _is_in_italic(node):
                continue
            if _is_in_ignored_container(node):
                continue

            href = node.get("href", "")
            if depth == 0 and _is_valid_article_href(href):
                href_title = _href_to_title(href)
                if _normalize_title(href_title) == current_key:
                    continue
                hrefs.append(href)

    return hrefs


def _fetch_page_title(session, url):
    soup, _ = _fetch_page(session, url)
    return _extract_main_title(soup), soup


def _find_first_valid_intro_link(session, soup, current_title, visited):
    hrefs = _collect_intro_link_hrefs(soup, current_title)
    if not hrefs:
        return None

    current_key = _normalize_title(current_title)
    for index, href in enumerate(hrefs):
        next_title, next_soup = _fetch_page_title(session, BASE_URL + href)
        if not next_title:
            continue

        next_key = _normalize_title(next_title)
        if next_key == current_key or next_key in visited:
            continue

        next_hrefs = _collect_intro_link_hrefs(next_soup, next_title)
        if next_hrefs:
            lookahead_title, _ = _fetch_page_title(session, BASE_URL + next_hrefs[0])
            if lookahead_title:
                lookahead_key = _normalize_title(lookahead_title)
                if lookahead_key == current_key or lookahead_key in visited:
                    if index + 1 < len(hrefs):
                        continue

        return href

    return None


def _fetch_page(session, url, params=None):
    response = session.get(url, params=params, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup, response.url


def _print_and_register(title, roads, visited):
    key = _normalize_title(title)
    if key in visited:
        print("It leads to an infinite loop !")
        return False, True
    visited.add(key)
    roads.append(title)
    print(title)
    if key == "philosophy":
        return True, False
    return False, False


def main():
    if len(sys.argv) != 2:
        print("Error: one search parameter is required.")
        return 1

    request_text = sys.argv[1].strip()
    if not request_text:
        print("Error: search parameter cannot be empty.")
        return 1

    session = requests.Session()
    session.headers.update({"User-Agent": "PiscineDjangoEx03/1.0"})

    roads = []
    visited = set()

    try:
        soup, current_url = _fetch_page(
            session,
            SEARCH_URL,
            params={"search": request_text, "title": "Special:Search", "go": "Go"},
        )

        max_hops = 1000
        for _ in range(max_hops):
            title = _extract_main_title(soup)
            if not title:
                print("Error: unable to parse Wikipedia page title.")
                return 1

            if _normalize_title(title) == "search results":
                print("It's a dead end !")
                return 0

            redirected_from = _extract_redirected_from(soup)
            if redirected_from:
                reached_philosophy, hit_loop = _print_and_register(redirected_from, roads, visited)
                if hit_loop:
                    return 0
                if reached_philosophy:
                    print(f"{len(roads)} roads from {request_text} to philosophy !")
                    return 0

            reached_philosophy, hit_loop = _print_and_register(title, roads, visited)
            if hit_loop:
                return 0
            if reached_philosophy:
                print(f"{len(roads)} roads from {request_text} to philosophy !")
                return 0

            href = _find_first_valid_intro_link(session, soup, title, visited)
            if not href:
                print("It leads to a dead end !")
                return 0

            soup, current_url = _fetch_page(session, BASE_URL + href)

        print("It leads to an infinite loop !")
        return 0
    except requests.RequestException:
        print("Error: unable to contact Wikipedia.")
        return 1
    except Exception:
        print("Error: an unexpected error occurred.")
        return 1


if __name__ == "__main__":
    sys.exit(main())