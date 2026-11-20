"""Regenerate static SEO markup from the public data and page copy. Run: py -3 scripts/build-seo.py"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://trattoriasantarita.dk"
BOOK = "https://book.trattoriasantarita.dk/book"
PHOTO = BASE + "/immagini/santa-rita-og.jpg"
PUBLIC = json.loads((ROOT / "dati-pubblici.json").read_text(encoding="utf-8"))

# The Danish entries are delivered in the HTML response. Other languages follow
# the existing client-side language selector and therefore need JavaScript.
COPY = {
    "index.html": {
        "da": ("Italiensk restaurant i Horsens | Trattoria Santa Rita", "Besøg Trattoria Santa Rita på Fugholm 12 i Horsens. Se vores italienske menukort, åbningstider og book et bord."),
        "it": ("Ristorante italiano a Horsens | Trattoria Santa Rita", "Vieni alla Trattoria Santa Rita in Fugholm 12 a Horsens. Scopri il menu italiano, gli orari e prenota un tavolo."),
        "en": ("Italian restaurant in Horsens | Trattoria Santa Rita", "Visit Trattoria Santa Rita at Fugholm 12 in Horsens. Explore our Italian menu, opening hours and table booking."),
    },
    "menu.html": {
        "da": ("Menukort i Horsens | Trattoria Santa Rita", "Se menukortet hos Trattoria Santa Rita i Horsens med antipasti, pasta, pizza og desserter."),
        "it": ("Menu italiano a Horsens | Trattoria Santa Rita", "Scopri il menu della Trattoria Santa Rita a Horsens: antipasti, pasta, pizza e dolci."),
        "en": ("Italian menu in Horsens | Trattoria Santa Rita", "Explore the Trattoria Santa Rita menu in Horsens, including antipasti, pasta, pizza and desserts."),
    },
    "shop.html": {
        "da": ("Shop under forberedelse | Trattoria Santa Rita", "Se idéer til Trattoria Santa Ritas kommende shop. Produkter og onlinebestilling er endnu ikke tilgængelige."),
        "it": ("Shop in preparazione | Trattoria Santa Rita", "Scopri le idee per il futuro shop della Trattoria Santa Rita. Prodotti e ordini online non sono ancora disponibili."),
        "en": ("Shop in preparation | Trattoria Santa Rita", "Explore ideas for the future Trattoria Santa Rita shop. Products and online ordering are not yet available."),
    },
    "vini.html": {
        "da": ("Vin under forberedelse | Trattoria Santa Rita", "Vinsektionen hos Trattoria Santa Rita er en forhåndsvisning. Udvalg og priser er endnu ikke fastlagt."),
        "it": ("Vini in preparazione | Trattoria Santa Rita", "La sezione vini della Trattoria Santa Rita è un'anteprima. Selezione e prezzi sono ancora da definire."),
        "en": ("Wine selection in preparation | Trattoria Santa Rita", "The Trattoria Santa Rita wine section is a preview. Selection and prices have yet to be confirmed."),
    },
    "cesti-regalo.html": {
        "da": ("Gavekurve under forberedelse | Trattoria Santa Rita", "Gavekurve hos Trattoria Santa Rita er endnu ikke til salg. Se forhåndsvisningen af mulige varianter."),
        "it": ("Cesti regalo in preparazione | Trattoria Santa Rita", "I cesti regalo della Trattoria Santa Rita non sono ancora in vendita. Guarda le possibili varianti in anteprima."),
        "en": ("Gift baskets in preparation | Trattoria Santa Rita", "Trattoria Santa Rita gift baskets are not yet for sale. Preview the possible options."),
    },
    "buoni-regalo.html": {
        "da": ("Gavekort under forberedelse | Trattoria Santa Rita", "Gavekort hos Trattoria Santa Rita er endnu ikke til salg online. Se forhåndsvisningen og kontakt restauranten."),
        "it": ("Buoni regalo in preparazione | Trattoria Santa Rita", "I buoni regalo della Trattoria Santa Rita non sono ancora acquistabili online. Guarda l'anteprima e contatta il ristorante."),
        "en": ("Gift cards in preparation | Trattoria Santa Rita", "Trattoria Santa Rita gift cards cannot yet be purchased online. View the preview and contact the restaurant."),
    },
    "carrello.html": {
        "da": ("Kurv uden onlinebestilling | Trattoria Santa Rita", "Se din kurv i Trattoria Santa Ritas shopforhåndsvisning. Ingen ordre eller betaling sendes."),
        "it": ("Carrello senza ordini online | Trattoria Santa Rita", "Visualizza il carrello nell'anteprima dello shop della Trattoria Santa Rita. Nessun ordine o pagamento viene inviato."),
        "en": ("Basket without online ordering | Trattoria Santa Rita", "View your basket in the Trattoria Santa Rita shop preview. No order or payment is submitted."),
    },
}

def esc(value: str) -> str:
    return html.escape(value, quote=True)

def canonical(page: str) -> str:
    return BASE + ("/" if page == "index.html" else "/" + page)

def meta_block(page: str) -> str:
    title, description = COPY[page]["da"]
    url = canonical(page)
    robots = "index,follow" if page in ("index.html", "menu.html") else "noindex,follow"
    lines = [
        f'<meta name="description" content="{esc(description)}">',
        f'<meta name="robots" content="{robots}">',
        f'<link rel="canonical" href="{url}">',
        '<link rel="icon" href="/immagini/favicon.png" type="image/png">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:site_name" content="{esc(PUBLIC["name"])}">',
        f'<meta property="og:locale" content="da_DK">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:image" content="{PHOTO}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(description)}">',
        f'<meta name="twitter:image" content="{PHOTO}">',
    ]
    if page == "index.html":
        schema = {
            "@context": "https://schema.org",
            "@type": "Restaurant",
            "name": PUBLIC["name"],
            "url": BASE + "/",
            "image": PHOTO,
            "address": {"@type": "PostalAddress", **{k: PUBLIC[k] for k in ("streetAddress", "postalCode", "addressLocality", "addressCountry")}},
            "telephone": PUBLIC["telephone"],
            "email": PUBLIC["email"],
            "hasMenu": canonical("menu.html"),
            "potentialAction": {"@type": "ReserveAction", "target": BOOK},
            "openingHoursSpecification": [
                {"@type": "OpeningHoursSpecification", "dayOfWeek": slot["days"], "opens": slot["opens"], "closes": slot["closes"]}
                for slot in PUBLIC["openingHours"]
            ],
        }
        lines.append('<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + '</script>')
    return '<!-- SEO: generated by scripts/build-seo.py -->\n' + '\n'.join(lines) + '\n<!-- /SEO -->'

def update_page(page: str) -> None:
    path = ROOT / page
    source = path.read_text(encoding="utf-8")
    head = re.search(r"(?is)<head\b[^>]*>(.*?)</head>", source)
    if not head:
        raise ValueError(f"Missing head: {page}")
    content = head.group(1)
    content = re.sub(r"(?is)<!-- SEO: generated by scripts/build-seo\.py -->.*?<!-- /SEO -->", "", content)
    content = re.sub(r"(?is)<title>.*?</title>", "", content, count=1)
    content = re.sub(r"(?is)<meta\b(?=[^>]*\bname=[\"']description[\"'])[^>]*>", "", content)
    content = re.sub(r"(?is)<link\b(?=[^>]*\brel=[\"']icon[\"'])[^>]*>", "", content)
    content = re.sub(r'(?is)<script\b(?=[^>]*src="seo-metadata\.js")[^>]*></script>', "", content)
    title = esc(COPY[page]["da"][0])
    content = f"\n<title>{title}</title>\n" + meta_block(page) + "\n" + content.strip() + '\n<script src="seo-metadata.js" defer></script>\n'
    source = source[:head.start(1)] + content + source[head.end(1):]
    if page == "index.html":
        hours = PUBLIC["openingHours"]
        assert [x["days"] for x in hours] == [["Tuesday", "Wednesday", "Thursday"], ["Friday"], ["Saturday"]]
        def time_range(slot: dict) -> str:
            return f'{esc(slot["opens"])} – {esc(slot["closes"])}'
        visible = ('<section class="visit-hours" aria-labelledby="visitHoursTitle"><h3 id="visitHoursTitle" data-i18n="hoursTitle">Åbningstider</h3><dl>'
                   '<div><dt data-i18n="hoursSunMon">Søndag – mandag</dt><dd data-i18n="hoursClosed">Lukket</dd></div>'
                   f'<div><dt data-i18n="hoursTueThu">Tirsdag – torsdag</dt><dd>{time_range(hours[0])}</dd></div>'
                   f'<div><dt data-i18n="hoursFriday">Fredag</dt><dd>{time_range(hours[1])}</dd></div>'
                   f'<div><dt data-i18n="hoursSaturday">Lørdag</dt><dd>{time_range(hours[2])}</dd></div></dl></section>')
        source, count = re.subn(r'(?is)<section class="visit-hours".*?</section>', lambda _: visible, source, count=1)
        assert count == 1
        phone = PUBLIC["telephone"]
        assert re.fullmatch(r"\+45\d{8}", phone), "Expected a Danish telephone number"
        display_phone = "+45 " + " ".join(phone[i:i + 2] for i in range(3, len(phone), 2))
        contact = (f'<p class="address"><strong>{esc(PUBLIC["name"])}</strong><br>{esc(PUBLIC["streetAddress"])}<br>{esc(PUBLIC["postalCode"])} {esc(PUBLIC["addressLocality"])}, <span data-site-text="country">Danmark</span></p>'
                   f'<div class="visit-contact"><a href="tel:{esc(phone)}"><span aria-hidden="true">☎</span> {esc(display_phone)}</a><a href="mailto:{esc(PUBLIC["email"])}"><span aria-hidden="true">✉</span> {esc(PUBLIC["email"])}</a></div>')
        source, count = re.subn(r'(?is)<p class="address">.*?</p>\s*<div class="visit-contact">.*?</div>', lambda _: contact, source, count=1)
        assert count == 1
    path.write_text(source, encoding="utf-8")

def runtime() -> None:
    copy = {page: {lang: {"title": title, "description": desc} for lang, (title, desc) in translations.items()} for page, translations in COPY.items()}
    script = ("/* Generated by scripts/build-seo.py; static Danish metadata remains in each HTML head. */\n"
              "(function(){const pages=" + json.dumps(copy, ensure_ascii=False, separators=(",", ":")) + ";"
              "const page=location.pathname.split('/').pop()||'index.html',entry=pages[page];if(!entry)return;"
              "function setMeta(selector,value){const el=document.querySelector(selector);if(el)el.setAttribute('content',value)}"
              "function update(){const lang=['da','it','en'].includes(document.documentElement.lang)?document.documentElement.lang:'da';"
              "const value=entry[lang];document.title=value.title;setMeta('meta[name=description]',value.description);"
              "setMeta('meta[property=\"og:title\"]',value.title);setMeta('meta[property=\"og:description\"]',value.description);"
              "setMeta('meta[property=\"og:locale\"]',({da:'da_DK',it:'it_IT',en:'en_GB'})[lang]);"
              "setMeta('meta[name=\"twitter:title\"]',value.title);setMeta('meta[name=\"twitter:description\"]',value.description)}"
              "if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',update);else update();"
              "new MutationObserver(update).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});})();\n")
    (ROOT / "seo-metadata.js").write_text(script, encoding="utf-8")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-cesti", action="store_true", help="Avoid the concurrent image edit")
    args = parser.parse_args()
    for page in COPY:
        if args.skip_cesti and page == "cesti-regalo.html":
            continue
        update_page(page)
    runtime()
