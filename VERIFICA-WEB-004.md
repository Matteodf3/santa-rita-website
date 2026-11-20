# WEB-004 — preparazione SEO e dati pubblici

## Implementato nella copia di sviluppo

- Titolo e descrizione distinti per le sette pagine, con danese statico nell'HTML e italiano/inglese aggiornati dal selettore tramite `seo-metadata.js`. Anche titolo e descrizione Open Graph/Twitter cambiano nel browser. I crawler e le anteprime che non eseguono JavaScript vedono il danese.
- Canonical scelto dall'utente: `https://trattoriasantarita.dk` senza `www`. Questo host è usato in canonical, Open Graph, sitemap e robots. Nessun `hreflang`: le tre lingue condividono gli stessi URL.
- `shop.html`, `vini.html`, `cesti-regalo.html`, `buoni-regalo.html` e `carrello.html` hanno `noindex,follow` e non compaiono nella sitemap mentre prodotti e ordini non sono operativi. Robots consente la scansione di queste pagine affinché i motori leggano il `noindex`.
- Foto OG 1200×630 derivata dalla foto originale della facciata; verificare i diritti d'uso prima del rilascio. Favicon su tutte le pagine, 404 trilingue, sitemap, robots e `deploy/.htaccess.example` di sola preparazione. Redirect esatti per i tre URL WordPress identificati e redirect `www` verso il dominio scelto; l'esempio va verificato sull'hosting prima di essere attivato.
- `dati-pubblici.json` è l'unica sorgente per contatti e orari del sito pubblico: `py -3 scripts/build-seo.py` rigenera markup visibile della home e schema Restaurant. L'indirizzo, telefono ed email corrispondono al sito attuale; gli orari riprendono la home attuale: domenica/lunedì chiuso, martedì–giovedì 16–21, venerdì 16–22, sabato 12–22. BOOK `/impostazioni` è ancora protetto: confronto con BOOK e conferma del responsabile del ristorante pendenti. Non sono stati inseriti geocoordinate, stelle o recensioni nello schema.

## Verifiche

- `py -3 tests/seo.py`: 4 test superati, su metadati statici e risorse, coerenza JSON-LD/orari visibili, sitemap/robots/404 e testo dei redirect esatti. La configurazione Apache non è stata provata sull'hosting.
- `node tests/lingua.cjs`: superato, preferenze lingua e persistenza.
- Il coordinatore ha verificato 168 combinazioni in Chrome con viewport emulato (7 pagine × 8 larghezze × 3 lingue): nessun overflow, lingua e menu mobile coerenti. Non è una prova su dispositivi fisici.
- Home verificata in browser in tre lingue: titolo, OG, canonical senza `www`, parametro BOOK e schema corretti. Nessuna risorsa remota richiesta all'avvio. Immagine OG esaminata a 1200×630.
- Pagina 404 verificata in browser in tre lingue: titolo, intestazione, link BOOK localizzato e selettore condiviso funzionanti. La risposta HTTP 404 effettiva dipende dalla configurazione dell'hosting.
- Misura cache vuota su HTTP locale senza compressione: desktop 1440×900 DPR 1, 504.797 byte (493,0 KiB) iniziali e 693.717 byte (677,5 KiB) dopo scorrimento; mobile 390×844 DPR 1, 380.273 byte (371,4 KiB) iniziali e 449.235 byte (438,7 KiB) dopo scorrimento. Entrambi i caricamenti iniziali sono sotto 500 KiB. La WebP hero è stata ottimizzata da 210.344 a 195.858 byte; l'originale resta intatto e il confronto visivo locale risulta simile.

## Prima del rilascio

Confermare gli orari in BOOK e con il ristorante, verificare diritti della foto, supporto e comportamento dei redirect su one.com, risposta HTTP 404 effettiva e anteprime social tramite gli strumenti di condivisione su URL pubblico (non verificabili sulla copia locale). Dopo ogni modifica agli orari: aggiornare prima BOOK, poi `dati-pubblici.json`, rigenerare e confrontare sito visibile/schema; annotare responsabile, data e confronto. Il gestore del profilo Google aggiorna separatamente gli orari Google Business Profile. Nessun deploy o modifica DNS/hosting è stato eseguito.
