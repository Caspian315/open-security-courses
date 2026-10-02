"""Check generated HTML links, anchors and assets, including Pages subpaths."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, bool]] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        attribute = {"a": "href", "link": "href", "script": "src", "img": "src"}.get(tag)
        if attribute and attrs.get(attribute):
            self.links.append((attrs[attribute], tag == "a"))


def check(site: Path, base_path: str) -> list[str]:
    base_path = "/" + base_path.strip("/") + "/" if base_path.strip("/") else "/"
    pages = {p.resolve(): Page(p.read_text(encoding="utf-8")) for p in site.rglob("*.html")}
    errors: list[str] = []
    for source, page in pages.items():
        relative_source = source.relative_to(site).as_posix()
        source_url = base_path + relative_source
        for link, check_anchor in page.links:
            parsed = urlsplit(link)
            # External URLs are tested separately when the site is published.
            if parsed.scheme or parsed.netloc:
                continue
            resolved = urlsplit(urljoin(source_url, link))
            if not resolved.path.startswith(base_path):
                errors.append(f"{relative_source}: link escapes Pages path: {link}")
                continue
            target = (site / unquote(resolved.path[len(base_path):])).resolve()
            if not target.is_relative_to(site):
                errors.append(f"{relative_source}: link escapes site directory: {link}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{relative_source}: missing target: {link}")
            elif check_anchor and resolved.fragment and target.suffix == ".html":
                fragment = unquote(resolved.fragment)
                target_page = pages.get(target)
                if target_page is not None and fragment not in target_page.ids:
                    errors.append(f"{relative_source}: missing anchor: {link}")
    print(f"Checked {len(pages)} HTML pages and {sum(len(p.links) for p in pages.values())} local/external references.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    parser.add_argument("--base-path", default="/open-security-courses/")
    args = parser.parse_args()
    site = args.site_dir.resolve()
    if not (site / "index.html").is_file():
        parser.error("Build the site with python -m mkdocs build --strict first.")
    errors = check(site, args.base_path)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("All internal links, anchors and local assets exist.")


if __name__ == "__main__":
    main()
