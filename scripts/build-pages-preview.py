"""Build an isolated GitHub Pages artifact. Never edits the production source files."""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = "https://matteodf3.github.io/santa-rita-website/"
PRODUCTION_BASE = "https://trattoriasantarita.dk"
HTML_FILES = (
    "index.html", "menu.html", "shop.html", "vini.html", "cesti-regalo.html",
    "buoni-regalo.html", "carrello.html", "404.html",
)
STATIC_FILES = (
    "lingua.js", "lingua.css", "inglese.js", "prenotazione.js",
    "carrello.js", "recensioni-google.js", "menu-dati.js",
    "menu-inglese.js", "menu-traduzioni.js", "seo-metadata.js",
)
ASSET = re.compile(r"(?<![A-Za-z0-9_])immagini/[A-Za-z0-9._/-]+\.(?:webp|png|jpe?g)", re.I)
ROOT_PATH = re.compile(r"(\b(?:href|src|action|poster)\s*=\s*)([\"'])(/(?!/))", re.I)
ROBOTS_META = re.compile(r"(?is)<meta\b(?=[^>]*\bname=[\"']robots[\"'])[^>]*>")
SCHEMA_SCRIPT = re.compile(r"(?is)<script\b(?=[^>]*\btype=[\"']application/ld\+json[\"'])[^>]*>.*?</script>")


def normalized_base(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("Preview base must be an HTTPS URL without query or fragment")
    if parsed.path.rstrip("/") != "/santa-rita-website":
        raise ValueError("Preview must be served from /santa-rita-website/")
    return value.rstrip("/") + "/"


def transform_html(source: str, base: str) -> str:
    if "<head" not in source.lower() or "</head>" not in source.lower():
        raise ValueError("HTML must contain a head")
    source = SCHEMA_SCRIPT.sub("", source)
    source = ROBOTS_META.sub("", source)
    source = re.sub(r"(?i)<head\b[^>]*>", lambda m: m.group(0) + '\n<meta name="robots" content="noindex,nofollow">', source, count=1)
    source = source.replace(PRODUCTION_BASE, base.rstrip("/"))
    source = ROOT_PATH.sub(lambda m: m.group(1) + m.group(2) + "/santa-rita-website/", source)
    return source


def build(destination: Path, base: str) -> None:
    base = normalized_base(base)
    if destination.is_symlink():
        raise ValueError("Artifact output must not be a symbolic link")
    destination = destination.resolve()
    if destination != ROOT / ".pages-preview":
        raise ValueError("Artifact output is restricted to the ignored .pages-preview folder")
    if destination.exists():
        if not destination.is_dir():
            raise ValueError("Artifact path must be a directory")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    image_names: set[str] = set()
    for name in HTML_FILES:
        source = (ROOT / name).read_text(encoding="utf-8")
        image_names.update(ASSET.findall(source))
        (destination / name).write_text(transform_html(source, base), encoding="utf-8")
    for name in STATIC_FILES:
        source = (ROOT / name).read_text(encoding="utf-8")
        image_names.update(ASSET.findall(source))
        (destination / name).write_text(source, encoding="utf-8")
    for name in sorted(image_names):
        source = ROOT / name
        if not source.is_file() or source.parent != ROOT / "immagini":
            raise ValueError(f"Referenced image missing or outside images root: {name}")
        target = destination / name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(source, target)
    (destination / ".nojekyll").write_bytes(b"")
    # A project-path robots.txt has limited crawler scope. HTML noindex is the gate.
    (destination / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    print(f"Built {destination} ({len(HTML_FILES)} HTML, {len(STATIC_FILES)} JS/CSS, {len(image_names)} images)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    args = parser.parse_args()
    build(ROOT / ".pages-preview", args.base_url)
