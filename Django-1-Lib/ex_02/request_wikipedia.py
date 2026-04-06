import requests, json, dewiki, sys

def _sanitize_filename(query):
    normalized = "_".join(query.strip().split())
    safe_chars = []
    for char in normalized:
        if char.isalnum() or char in "_-":
            safe_chars.append(char)
        else:
            safe_chars.append("_")
    result = "".join(safe_chars).strip("_")
    return result


def _normalize_for_match(text):
    return "".join(char.lower() for char in text if char.isalnum())


def _tokenize_for_match(text):
    cleaned = []
    for char in text.lower():
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append(" ")
    return [token for token in "".join(cleaned).split() if token]


def _pick_best_title(query, search_results):
    if not search_results:
        return None

    normalized_query = _normalize_for_match(query)
    query_tokens = _tokenize_for_match(query)
    best_title = None
    best_score = -1

    for result in search_results:
        title = result.get("title", "")
        if not title:
            continue

        normalized_title = _normalize_for_match(title)
        title_tokens = _tokenize_for_match(title)
        overlap = 0
        for token in query_tokens:
            if token in title_tokens:
                overlap += 1

        score = overlap
        if normalized_query and normalized_query == normalized_title:
            score += 10
        elif normalized_query and normalized_query in normalized_title:
            score += 5

        if score > best_score:
            best_score = score
            best_title = title

    if best_score <= 0:
        return None
    return best_title


def _search_best_title(session, url, query):
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 5,
        "srinfo": "suggestion",
    }
    response = session.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    query_data = data.get("query", {})
    search_results = query_data.get("search", [])
    best_title = _pick_best_title(query, search_results)
    if best_title:
        return best_title

    suggestion = query_data.get("searchinfo", {}).get("suggestion")
    if not suggestion:
        return None

    params["srsearch"] = suggestion
    response = session.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    search_results = data.get("query", {}).get("search", [])
    return _pick_best_title(suggestion, search_results)


def _fetch_extract(session, url, title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": 1,
        "redirects": 1,
        "titles": title,
    }
    response = session.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    extract = page.get("extract", "").strip()
    if not extract:
        return None
    return dewiki.from_string(extract).strip()


def main():
    if len(sys.argv) != 2:
        print("Error: one search parameter is required.")
        return 1

    query = sys.argv[1].strip()
    if not query:
        print("Error: search parameter cannot be empty.")
        return 1

    filename_root = _sanitize_filename(query)
    if not filename_root:
        print("Error: invalid search parameter for filename.")
        return 1

    api_urls = [
        "https://fr.wikipedia.org/w/api.php",
        "https://en.wikipedia.org/w/api.php",
    ]

    try:
        session = requests.Session()
        session.headers.update({"User-Agent": "PiscineDjangoEx02/1.0"})

        last_request_error = None
        content = None
        title = None
        for api_url in api_urls:
            try:
                # Try exact title first to avoid unrelated top search hits.
                content = _fetch_extract(session, api_url, query)
                if content:
                    break

                title = _search_best_title(session, api_url, query)
                if not title:
                    continue
                content = _fetch_extract(session, api_url, title)
                if content:
                    break
            except requests.RequestException as request_error:
                last_request_error = request_error
                continue

        if content:
            pass
        elif title:
            print("Error: Wikipedia content not found.")
            return 1
        elif last_request_error is not None:
            print("Error: unable to contact Wikipedia API.")
            return 1
        else:
            print("Error: no matching Wikipedia page found.")
            return 1
    except json.JSONDecodeError:
        print("Error: invalid response from Wikipedia API.")
        return 1
    except Exception:
        print("Error: an unexpected problem occurred.")
        return 1

    output_file = filename_root + ".wiki"
    try:
        with open(output_file, "w", encoding="utf-8") as file_handle:
            file_handle.write(content)
    except OSError:
        print("Error: unable to write output file.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())