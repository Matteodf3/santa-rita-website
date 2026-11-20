# WEB-002 — verifica del 20/11/2026

Stato: implementazione locale completata, da verificare su BOOK autenticato prima di dichiarare la milestone fatta.

## Modifiche

- 10 collegamenti di prenotazione sulle sette pagine: destinazione `https://book.trattoriasantarita.dk/book?lang=...`, aggiornata quando cambia la lingua del documento. Il collegamento funziona anche senza JavaScript nella lingua danese predefinita.
- Rimossi dialoghi e codice della vecchia prenotazione dimostrativa. Nessuna striscia di anteprima presente.
- Due immagini incorporate condivise (logo e sfondo) estratte in file separati; originali conservati in `immagini/originali`.
- Varianti WebP con `srcset`, `sizes`, larghezza/altezza dichiarate; immagini sotto la prima schermata differite; logo e sfondo iniziale caricati subito. Foto principali originali conservate. Alcune immagini dinamiche dei cesti restano URL remoti: non sono immagini incorporate nell’HTML.
- Nessuna traduzione inglese completa aggiunta: è WEB-003. Il generatore dei link gestisce già da/it/en, verificato separatamente dalla traduzione dell’interfaccia.

## Verificato

- `node --check` su script esterni e script inline estratti: PASS.
- Controllo automatico: nessun `data:image` o `bookingDialog` nelle pagine.
- Browser Chrome locale, server Python su `127.0.0.1:8087`: sette pagine, viewport CSS 390×844, 820×1180 e 1440×900; nessun overflow orizzontale rilevato. Intercettazione errori JavaScript a 390 pixel: nessun errore.
- Collegamenti da/it/en controllati su ogni pagina cambiando la lingua del documento: tutti corretti. Non equivale alla presenza della lingua inglese nel selettore.
- Home senza scorrimento, cache ignorata al ricaricamento: 364478 byte (circa 356 KiB) a 390×844; 477852 byte (circa 467 KiB) a 1440×900, misurati con Resource/Navigation Timing. Test DPR 1: le misure non garantiscono lo stesso risultato su tutti i dispositivi, connessioni o DPR. Nessuna compressione HTTP aggiuntiva sul server Python.
- File HTML home: 3217793 → 53482 byte; shop: 3204617 → 39848 byte. La dimensione HTML non è il traffico totale della pagina.
- Prima schermata desktop osservata nello screenshot: logo, foto di sfondo, testo e pulsanti presenti.

## Limiti e lavoro aperto

- Apertura BOOK in contesto browser isolato: `net::ERR_INVALID_AUTH_CREDENTIALS`. Nessuna prenotazione effettuata. La pagina di destinazione e la lingua da/it/en devono essere provate con accesso valido.
- Prove emulate, non su iPad o telefono fisici. Non eseguita una revisione visiva completa di tutte le sezioni e di tutti i form.
- Peso completo dopo scorrimento ancora da misurare; alcuni contenuti dinamici remoti restano da ottimizzare in WEB-005.
- Nessun deploy. Cartella sul Desktop e sito pubblico invariati.
