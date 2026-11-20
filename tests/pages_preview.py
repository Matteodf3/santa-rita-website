"""Build and verify the manual GitHub Pages artifact: py -3 tests/pages_preview.py"""
from __future__ import annotations

import importlib.util
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_pages_preview", ROOT / "scripts" / "build-pages-preview.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ARTIFACT = ROOT / ".pages-preview"
BASE = MODULE.DEFAULT_BASE


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if attrs.get(key):
                self.paths.append(attrs[key])
        if attrs.get("srcset"):
            self.paths += [part.strip().split()[0] for part in attrs["srcset"].split(",")]


class PreviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        MODULE.build(ARTIFACT, BASE)

    def test_exact_pack_and_secret_scan(self):
        expected = set(MODULE.HTML_FILES) | set(MODULE.STATIC_FILES) | {"robots.txt", ".nojekyll"}
        expected |= set().union(*(set(MODULE.ASSET.findall((ROOT / name).read_text(encoding="utf-8"))) for name in MODULE.HTML_FILES + MODULE.STATIC_FILES))
        actual = {path.relative_to(ARTIFACT).as_posix() for path in ARTIFACT.rglob("*") if path.is_file()}
        self.assertEqual(actual, expected)
        self.assertNotIn("sitemap.xml", actual)
        self.assertNotIn("CNAME", actual)
        self.assertFalse(any("originali/" in name or "tests/" in name or "docs/" in name or ".git/" in name for name in actual))
        for path in ARTIFACT.rglob("*"):
            if path.suffix in {".html", ".js", ".css", ".txt"}:
                content = path.read_text(encoding="utf-8")
                self.assertNotRegex(content, r"(?i)(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16})", path.name)

    def test_rejects_other_output_without_touching_it(self):
        marker = ROOT / "scripts" / "build-seo.py"
        before = marker.read_bytes()
        with self.assertRaises(ValueError):
            MODULE.build(ROOT / "scripts", BASE)
        self.assertEqual(marker.read_bytes(), before)

    def test_html_preview_metadata_and_links(self):
        for name in MODULE.HTML_FILES:
            with self.subTest(page=name):
                content = (ARTIFACT / name).read_text(encoding="utf-8")
                self.assertEqual(len(re.findall(r'(?i)<meta\s+name="robots"\s+content="noindex,nofollow"', content)), 1)
                self.assertNotIn("application/ld+json", content)
                self.assertNotIn(MODULE.PRODUCTION_BASE, content)
                self.assertNotIn("www.matteodf3.github.io", content)
                if name != "404.html":
                    for selector in (r'<link rel="canonical" href="([^"]+)"', r'<meta property="og:url" content="([^"]+)"', r'<meta property="og:image" content="([^"]+)"'):
                        value = re.search(selector, content).group(1)
                        self.assertTrue(value.startswith(BASE), value)
                refs = References()
                refs.feed(content)
                refs.paths += re.findall(r'url\([\"\']?([^\)\"\']+)', content)
                for ref in refs.paths:
                    parsed = urlparse(ref)
                    if parsed.scheme or ref.startswith("#") or not parsed.path:
                        continue
                    if ref.startswith("/"):
                        self.assertTrue(ref.startswith("/santa-rita-website/"), ref)
                        local = parsed.path.removeprefix("/santa-rita-website/") or "index.html"
                    else:
                        local = parsed.path
                    self.assertTrue((ARTIFACT / local).is_file(), f"{name}: {ref}")
        error = (ARTIFACT / "404.html").read_text(encoding="utf-8")
        self.assertIn('href="/santa-rita-website/"', error)
        self.assertIn('href="/santa-rita-website/menu.html"', error)
        self.assertIn('src="/santa-rita-website/lingua.js"', error)
        self.assertIn('href="/santa-rita-website/lingua.css"', error)
        robots = (ARTIFACT / "robots.txt").read_text(encoding="utf-8")
        self.assertEqual(robots, "User-agent: *\nAllow: /\n")


if __name__ == "__main__":
    unittest.main()
