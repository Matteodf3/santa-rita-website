# Santa Rita Website

Sito pubblico in sviluppo: homepage, menu e shop. Questa repository privata conserva la cronologia della copia di lavoro. Il sito pubblico e il gestionale sono separati.

La prima revisione conserva il sito locale esistente senza modificarne il comportamento. Nessuna pubblicazione automatica configurata.

## Avvio locale

Dalla cartella della copia di lavoro: `py -3 -m http.server 8080 --bind 127.0.0.1`, quindi aprire `http://127.0.0.1:8080`. Lo stesso indirizzo locale permette di condividere lingua e carrello tra le pagine; il comportamento di localStorage con file aperti direttamente può variare tra browser.

## Lavoro

Sviluppare sui branch `t/WEB-NNN-descrizione`; tenere le modifiche verificate in commit piccoli. I commit e i push in questa repository non devono attivare alcun deploy finché non viene configurato e approvato. Non inserire credenziali o copie del database.

Vedere [MILESTONE.md](MILESTONE.md).
