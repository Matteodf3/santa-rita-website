"""Offline release checks: py -3 tests/seo.py"""
import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://trattoriasantarita.dk"
PAGES = ["index.html", "menu.html", "shop.html", "vini.html", "cesti-regalo.html", "buoni-regalo.html", "carrello.html"]
INDEXABLE = {"index.html", "menu.html"}
PUBLIC = json.loads((ROOT / "dati-pubblici.json").read_text(encoding="utf-8"))

def head(page):
    source = (ROOT / page).read_text(encoding="utf-8")
    return re.search(r"(?is)<head\b[^>]*>(.*?)</head>", source).group(1)

def attr(tag, name):
    match = re.search(rf'\b{name}="([^"]*)"', tag)
    return match.group(1) if match else None

def matching_tag(source, name, key, value):
    for tag in re.findall(rf"(?is)<{name}\b[^>]*>", source):
        if attr(tag, key) == value:
            return tag
    return None

class SeoTest(unittest.TestCase):
    def test_static_metadata_and_resources(self):
        titles, descriptions, canonicals = set(), set(), set()
        for page in PAGES:
            with self.subTest(page=page):
                content = head(page)
                title = re.search(r"(?is)<title>(.*?)</title>", content).group(1)
                desc = attr(matching_tag(content, "meta", "name", "description"), "content")
                self.assertTrue(desc and len(desc) > 50)
                titles.add(title)
                descriptions.add(desc)
                canonical = attr(matching_tag(content, "link", "rel", "canonical"), "href")
                self.assertEqual(canonical, BASE + ("/" if page == "index.html" else "/" + page))
                canonicals.add(canonical)
                self.assertEqual(attr(matching_tag(content, "meta", "property", "og:url"), "content"), canonical)
                self.assertEqual(attr(matching_tag(content, "meta", "property", "og:title"), "content"), title)
                self.assertEqual(attr(matching_tag(content, "meta", "name", "twitter:title"), "content"), title)
                self.assertEqual(attr(matching_tag(content, "meta", "name", "robots"), "content"), "index,follow" if page in INDEXABLE else "noindex,follow")
                self.assertIsNone(matching_tag(content, "link", "rel", "alternate"), "Same-URL hreflang must not be emitted")
                for rel in ("icon",):
                    path = attr(matching_tag(content, "link", "rel", rel), "href")
                    self.assertTrue((ROOT / path.lstrip("/")).is_file(), path)
                for property_name in ("og:image",):
                    url = attr(matching_tag(content, "meta", "property", property_name), "content")
                    self.assertEqual(urlparse(url).netloc, urlparse(BASE).netloc)
                    self.assertTrue((ROOT / urlparse(url).path.lstrip("/")).is_file())
                self.assertIn('src="seo-metadata.js"', content)
        self.assertEqual(len(titles), 7)
        self.assertEqual(len(descriptions), 7)
        self.assertEqual(len(canonicals), 7)

    def test_restaurant_schema_matches_visible_hours(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        schema = json.loads(re.search(r'(?s)<script type="application/ld\+json">(.*?)</script>', home).group(1))
        self.assertEqual(schema["@type"], "Restaurant")
        for field in ("name", "telephone", "email"):
            self.assertEqual(schema[field], PUBLIC[field])
        for field in ("streetAddress", "postalCode", "addressLocality", "addressCountry"):
            self.assertEqual(schema["address"][field], PUBLIC[field])
        self.assertEqual(schema["hasMenu"], BASE + "/menu.html")
        self.assertEqual(schema["potentialAction"]["target"], "https://book.trattoriasantarita.dk/book")
        self.assertNotIn("aggregateRating", schema)
        self.assertNotIn("geo", schema)
        slots = schema["openingHoursSpecification"]
        self.assertEqual(len(slots), len(PUBLIC["openingHours"]))
        visible = re.search(r'(?s)<section class="visit-hours".*?</section>', home).group(0)
        for slot, expected in zip(slots, PUBLIC["openingHours"]):
            self.assertEqual(slot["dayOfWeek"], expected["days"])
            self.assertEqual((slot["opens"], slot["closes"]), (expected["opens"], expected["closes"]))
            self.assertIn(expected["opens"] + " – " + expected["closes"], visible)
        self.assertIn(PUBLIC["email"], home)
        self.assertIn('href="tel:' + PUBLIC["telephone"] + '"', home)

    def test_sitemap_robots_and_error_page(self):
        sitemap = ET.parse(ROOT / "sitemap.xml")
        urls = {node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
        self.assertEqual(urls, {BASE + "/", BASE + "/menu.html"})
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: " + BASE + "/sitemap.xml", robots)
        for page in set(PAGES) - INDEXABLE:
            self.assertNotIn("Disallow: /" + page, robots, "Crawler must see the noindex meta tag")
        error = (ROOT / "404.html").read_text(encoding="utf-8")
        self.assertIn('content="noindex,follow"', error)
        self.assertIn("https://book.trattoriasantarita.dk/book?lang=da", error)
        self.assertIn("/menu.html", error)
        self.assertIn("Italiano", error)
        self.assertIn("English", error)

    def test_redirect_template_is_narrow_and_preserves_fragments(self):
        rules = (ROOT / "deploy" / ".htaccess.example").read_text(encoding="utf-8")
        self.assertIn("ErrorDocument 404 /404.html", rules)
        self.assertIn(r"RewriteCond %{HTTP_HOST} ^www\.trattoriasantarita\.dk$ [NC]", rules)
        for source, target, flags in (
            (r"^index\.php/menu/?$", "/menu.html", "[R=301,L,NC]"),
            (r"^index\.php/gallery/?$", "/#about", "[R=301,L,NC,NE]"),
            (r"^index\.php/kontakt-os/?$", "/#contact", "[R=301,L,NC,NE]"),
        ):
            self.assertIn(f"RewriteRule {source} {target} {flags}", rules)
        legacy = [line for line in rules.splitlines() if line.startswith("RewriteRule ^index")]
        self.assertEqual(len(legacy), 3, "No broad /index.php catch-all")

if __name__ == "__main__":
    unittest.main()
