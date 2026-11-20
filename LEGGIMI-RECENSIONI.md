# Carosello recensioni Google — anteprima locale

La sorgente è disattivata (`CONFIG.endpoint = null` in `recensioni-google.js`). La pagina non effettua richieste e non contiene recensioni inventate; il link usa il Place ID presente nella scheda di Byen Horsens (https://byenhorsens.dk/bedste/restauranter); l’apertura della scheda Google e della sezione recensioni va verificata nel browser.

## Collegamento futuro

Prima di attivare: scegliere una soluzione Places API autorizzata, verificare termini applicabili, attribuzione Google e degli autori, ordinamento, link alle singole recensioni, restrizioni su conservazione, privacy, quote e costi. Non assumere che un aggiornamento giornaliero con salvataggio dei testi sia consentito. Non inserire chiavi, token o credenziali nel browser o nei file dell’anteprima.

Il componente può leggere un endpoint HTTP(S) della stessa origine configurato in `CONFIG.endpoint`, non attivo ora. Contratto JSON: `{"reviews":[{"author":"...","rating":5,"text":"...","date":"...","reviewUrl":"https://...","authorUrl":"https://...","photoUrl":"https://...","translated":false}]}`. Al massimo cinque recensioni; autore, voto e collegamento Google della singola recensione sono obbligatori. Non memorizza dati nel browser. L'integrazione effettiva, inclusi origine e collegamento alla pagina recensioni esatta, deve essere verificata contro le condizioni Google correnti prima della pubblicazione.
