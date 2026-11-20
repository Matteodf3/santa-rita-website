# WEB-003 — tre lingue e selettore

Verifica locale del 20/11/2026. Nessuna pubblicazione.

## Realizzato

- Dansk, Italiano, English selezionabili su tutte e sette le pagine, con controllo nativo arrotondato, icona del globo, focus visibile e area di tocco mobile di 46 px.
- Nessuna scelta salvata: usare la prima lingua supportata indicata in `navigator.languages`, considerando varianti regionali come en-GB e it-IT. Se nessuna corrisponde, usare danese.
- La scelta manuale è salvata in localStorage e prevale sul browser; il rilevamento automatico non viene salvato come scelta manuale. In caso di storage non accessibile non bloccare la pagina.
- Interfaccia, messaggi, categorie, riepiloghi e descrizioni inglesi dei 47 piatti. Nomi italiani dei piatti mantenuti dove appropriato. Prezzi invariati. Traduzioni da rivedere con il ristorante prima della pubblicazione.
- Lingua trasmessa anche ai link BOOK; BOOK resta protetto e la pagina remota è da verificare quando sarà pubblica.

## Verifiche eseguite

- `node tests/lingua.cjs`: PASS. Rilevamento, precedenza della scelta, ricaricamento, lingua non supportata, storage indisponibile.
- `node --check` su script e script inline estratti, controllo esistenza risorse locali: PASS.
- Chrome locale, preferenze browser simulate con navigator.languages: en-GB → en; it-IT → it; da-DK → da; fr-FR → da; de-DE/en-US → en. Nessuna preferenza automatica salvata.
- Scelta esplicita English tramite evento del selettore: resta inglese nelle sette pagine e al ricaricamento, anche con browser simulato da-DK o it-IT.
- Aggiunto un buono nel carrello di prova: conferma e riepilogo in inglese; link BOOK con lang=en. Nessun ordine inviato.
- Sette pagine a 390 px: nessun errore JavaScript intercettato, nessun testo undefined o chiave visuale vuota rilevata, nessun overflow orizzontale. Sette pagine a 851 px: nessun overflow. Selettore mobile osservato nello screenshot con menu aperto; vista desktop osservata sulla home.

## Limiti

Preferenze emulate, non un cambio reale della lingua del sistema operativo. Nessun test su iPad/telefono fisici, lettore schermo o revisione linguistica professionale. Il selettore usa ora un pannello personalizzato; il controllo nativo è mantenuto come compatibilità senza JavaScript. L’inglese completo si prova nell’anteprima locale; non è stato messo online.

## Selettore personalizzato

Sostituito il menu nativo aperto con un pannello avorio/vino, nomi delle lingue, sigle e indicazione corrente. Provati nel browser: cambio English, salvataggio e BOOK lang=en; Home/freccia giù/Escape con ritorno focus; chiusura con clic esterno; pannello entro viewport mobile 390 px. Sintassi e test lingua nuovamente PASS. Nessun dispositivo fisico provato.
